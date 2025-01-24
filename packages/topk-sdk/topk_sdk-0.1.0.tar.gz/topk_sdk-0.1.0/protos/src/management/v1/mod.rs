use crate::control::v1::Index;

include!(concat!(env!("OUT_DIR"), "/topk.management.v1.rs"));

impl From<Index> for Collection {
    fn from(index: Index) -> Self {
        Self {
            name: index.name,
            org_id: index.org_id,
            project_id: index.project_id,
            schema: index.schema.into(),
        }
    }
}
