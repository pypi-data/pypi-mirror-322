use crate::{
    control::v1::index_service_client::IndexServiceClient,
    data::v1::{
        document_service_client::DocumentServiceClient, query_service_client::QueryServiceClient,
    },
};
use std::collections::HashMap;
use std::str::FromStr;
use tonic::{
    metadata::AsciiMetadataValue,
    service::{interceptor::InterceptedService, Interceptor},
    transport::Channel,
    Status,
};

pub struct AppendHeadersInterceptor {
    headers: HashMap<&'static str, String>,
}

impl Interceptor for AppendHeadersInterceptor {
    fn call(&mut self, mut request: tonic::Request<()>) -> Result<tonic::Request<()>, Status> {
        for (key, value) in self.headers.clone().into_iter() {
            request
                .metadata_mut()
                .insert(key, AsciiMetadataValue::from_str(value.as_str()).unwrap());
        }

        Ok(request)
    }
}

pub type DocumentClient = DocumentServiceClient<Channel>;
pub type DocumentClientWithHeaders =
    DocumentServiceClient<InterceptedService<Channel, AppendHeadersInterceptor>>;

impl DocumentClient {
    pub fn with_headers(
        channel: Channel,
        headers: HashMap<&'static str, String>,
    ) -> DocumentClientWithHeaders {
        Self::with_interceptor(channel, AppendHeadersInterceptor { headers })
    }
}

pub type QueryClient = QueryServiceClient<Channel>;
pub type QueryClientWithHeaders =
    QueryServiceClient<InterceptedService<Channel, AppendHeadersInterceptor>>;

impl QueryClient {
    pub fn with_headers(
        channel: Channel,
        headers: HashMap<&'static str, String>,
    ) -> QueryClientWithHeaders {
        Self::with_interceptor(channel, AppendHeadersInterceptor { headers })
    }
}

pub type IndexClient = IndexServiceClient<Channel>;
pub type IndexClientWithHeaders =
    IndexServiceClient<InterceptedService<Channel, AppendHeadersInterceptor>>;

impl IndexClient {
    pub fn with_headers(
        channel: Channel,
        headers: HashMap<&'static str, String>,
    ) -> IndexClientWithHeaders {
        Self::with_interceptor(channel, AppendHeadersInterceptor { headers })
    }
}
