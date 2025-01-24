use crate::{OrgId, ProjectId};
use uuid::Uuid;

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub struct IndexRef {
    pub org_id: OrgId,
    pub project_id: ProjectId,
    pub internal_id: uuid::Uuid,
}

impl IndexRef {
    pub fn new(org_id: OrgId, project_id: ProjectId, internal_id: uuid::Uuid) -> Self {
        IndexRef {
            org_id,
            project_id,
            internal_id,
        }
    }

    pub fn org_id(&self) -> OrgId {
        self.org_id
    }

    pub fn project_id(&self) -> ProjectId {
        self.project_id
    }

    pub fn internal_id(&self) -> Uuid {
        self.internal_id
    }

    /// Returns the data path form this index in the following form:
    /// `/org/{org_id}/project/{project_id}/index/{internal_id}`
    pub fn data_path(&self) -> String {
        format!(
            "/org/{}/project/{}/index/{}",
            self.org_id, self.project_id, self.internal_id,
        )
    }
}
