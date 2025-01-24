use super::*;

impl Index {
    pub fn new(
        name: impl Into<String>,
        org_id: u32,
        project_id: u32,
        schema: index_schema::IndexSchema,
    ) -> Self {
        Index {
            name: name.into(),
            org_id,
            project_id,
            schema: schema.into_fields(),
        }
    }
}
