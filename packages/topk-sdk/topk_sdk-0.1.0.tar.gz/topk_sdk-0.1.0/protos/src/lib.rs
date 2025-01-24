pub mod utils;

mod control;
mod data;
mod management;

pub mod v1 {
    pub use super::control::v1 as control;
    pub use super::data::v1 as data;
    pub use super::management::v1 as management;
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize, PartialEq, Eq, Hash)]
pub struct OrgId(u32);

impl OrgId {
    pub const fn new(value: u32) -> Self {
        Self(value)
    }
}

impl std::fmt::Display for OrgId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl From<u32> for OrgId {
    fn from(value: u32) -> Self {
        Self(value)
    }
}

impl From<OrgId> for u32 {
    fn from(value: OrgId) -> Self {
        value.0
    }
}

#[derive(Debug, Clone, Copy, serde::Serialize, serde::Deserialize, PartialEq, Eq, Hash)]
pub struct ProjectId(u32);

impl ProjectId {
    pub const fn new(value: u32) -> Self {
        Self(value)
    }
}

impl std::fmt::Display for ProjectId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl From<u32> for ProjectId {
    fn from(value: u32) -> Self {
        Self(value)
    }
}

impl From<ProjectId> for u32 {
    fn from(value: ProjectId) -> Self {
        value.0
    }
}
