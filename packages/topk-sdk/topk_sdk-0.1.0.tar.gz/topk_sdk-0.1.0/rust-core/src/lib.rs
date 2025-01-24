use std::{collections::HashMap, str::FromStr, time::Duration};
use tonic::transport::{Channel, Endpoint};
use topk_protos::{
    utils::{DocumentClient, QueryClient, QueryClientWithHeaders},
    v1::{
        control::{
            index_schema::IndexSchema, index_service_client::IndexServiceClient, index_slug,
            CreateIndexRequest, DeleteIndexRequest, Index, ListIndexesRequest,
        },
        data::{DeleteDocumentsRequest, Document, Query, QueryRequest, UpsertDocumentsRequest},
    },
};

mod internal_error_code;
pub use internal_error_code::InternalErrorCode;

pub mod macros;

#[derive(Debug, Clone)]
pub struct ClientConfig {
    pub api_key: String,
    pub region: Option<String>,
}

impl ClientConfig {
    pub fn api_key(&self) -> &str {
        &self.api_key
    }
}

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("lsn timeout")]
    LsnTimeout,

    #[error("not found")]
    NotFound,

    #[error("already exists")]
    AlreadyExists,

    #[error("internal error")]
    Internal,

    #[error("tonic error")]
    Unexpected(tonic::Status),

    #[error("tonic transport error")]
    TransportError(#[from] tonic::transport::Error),
}

impl From<tonic::Status> for Error {
    fn from(status: tonic::Status) -> Self {
        match status.code() {
            tonic::Code::NotFound => Self::NotFound,
            tonic::Code::AlreadyExists => Self::AlreadyExists,
            tonic::Code::Internal => Self::Internal,
            _ => Self::Unexpected(status),
        }
    }
}

#[derive(Clone)]
pub struct Client {
    config: ClientConfig,

    headers: HashMap<&'static str, String>,
}

impl Client {
    pub fn new(api_key: String, region: Option<String>) -> Self {
        Self {
            headers: HashMap::from([("authorization", format!("Bearer {}", api_key.clone()))]),
            config: ClientConfig { api_key, region },
        }
    }

    pub async fn query(&self, index: Index, query: Query) -> Result<Vec<Document>, Error> {
        let client =
            QueryClient::with_headers(connect_to_index(&index).await?, self.headers.clone());

        retry_query(client, query, None).await
    }

    pub async fn query_at_lsn(
        &self,
        index: Index,
        query: Query,
        lsn: u64,
    ) -> Result<Vec<Document>, Error> {
        let client =
            QueryClient::with_headers(connect_to_index(&index).await?, self.headers.clone());

        retry_query(client, query, Some(lsn)).await
    }

    pub async fn upsert(&self, index: Index, docs: Vec<Document>) -> Result<u64, Error> {
        let mut client =
            DocumentClient::with_headers(connect_to_index(&index).await?, self.headers.clone());

        let response = client
            .upsert_documents(UpsertDocumentsRequest { docs })
            .await?;

        Ok(response.into_inner().lsn)
    }

    pub async fn delete(&self, index: Index, ids: Vec<String>) -> Result<u64, Error> {
        let mut client =
            DocumentClient::with_headers(connect_to_index(&index).await?, self.headers.clone());

        let response = client
            .delete_documents(DeleteDocumentsRequest { ids })
            .await?;

        Ok(response.into_inner().lsn)
    }

    pub async fn query_blocking(
        &self,
        index: Index,
        query: Query,
        lsn: u64,
    ) -> Result<Vec<Document>, Error> {
        let mut client =
            QueryClient::with_headers(connect_to_index(&index).await?, self.headers.clone());

        let response = client
            .query(QueryRequest {
                query: Some(query),
                required_lsn: Some(lsn),
            })
            .await?;

        Ok(response.into_inner().results)
    }

    pub async fn list_indexes(&self) -> Result<Vec<Index>, Error> {
        let channel = connect_to_control_plane(&self.config).await?;

        let response = IndexServiceClient::with_headers(channel, self.headers.clone())
            .list_indexes(ListIndexesRequest {})
            .await?;

        Ok(response.into_inner().indexes)
    }

    pub async fn create_index(
        &self,
        name: impl Into<String>,
        schema: IndexSchema,
    ) -> Result<Index, Error> {
        let channel = connect_to_control_plane(&self.config).await?;

        let response = IndexServiceClient::new(channel)
            .create_index(CreateIndexRequest {
                name: name.into(),
                schema: schema.into_fields(),
            })
            .await?;

        Ok(response.into_inner().index.expect("invalid proto"))
    }

    pub async fn delete_index(&self, name: impl Into<String>) -> Result<(), Error> {
        let channel = connect_to_control_plane(&self.config).await?;

        IndexServiceClient::new(channel)
            .delete_index(DeleteIndexRequest { name: name.into() })
            .await?;

        Ok(())
    }
}

async fn connect_to_index(index: &Index) -> Result<Channel, Error> {
    let host = format!(
        "http://{}.index.ddb:8080",
        index_slug::encode(
            index.name.clone(),
            index.org_id.into(),
            index.project_id.into()
        )
        .expect("could not encode index slug")
    );

    Ok(Endpoint::from_str(&host)?.connect().await?)
}

async fn connect_to_control_plane(_config: &ClientConfig) -> Result<Channel, Error> {
    Ok(Endpoint::from_str("http://control.ddb:8080")?
        .connect()
        .await?)
}

async fn retry_query(
    mut client: QueryClientWithHeaders,
    query: Query,
    lsn: Option<u64>,
) -> Result<Vec<Document>, Error> {
    let mut tries = 0;
    let max_tries = 10;
    let retry_after = Duration::from_secs(1);

    loop {
        tries += 1;

        let query = query.clone();

        let response = client
            .query(QueryRequest {
                query: Some(query),
                required_lsn: lsn,
            })
            .await;

        match response {
            Ok(response) => return Ok(response.into_inner().results),
            Err(e) => {
                let code = InternalErrorCode::parse_status(&e);

                match code {
                    Ok(InternalErrorCode::RequiredLsnGreaterThanManifestMaxLsn) => {
                        if tries < max_tries {
                            tokio::time::sleep(retry_after).await;

                            continue;
                        } else {
                            return Err(Error::LsnTimeout);
                        }
                    }
                    _ => return Err(Error::Unexpected(e)),
                }
            }
        }
    }
}
