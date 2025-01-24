use crate::{OrgId, ProjectId};

pub fn encode(
    name: impl AsRef<str>,
    org_id: OrgId,
    project_id: ProjectId,
) -> Result<String, anyhow::Error> {
    if name.as_ref().is_empty() {
        return Err(anyhow::anyhow!("invalid index name"));
    }

    let org_id: u32 = org_id.into();
    let org_id = base32::encode(
        base32::Alphabet::Rfc4648Lower { padding: false },
        &org_id.to_le_bytes(),
    );
    assert!(org_id.len() == 7);

    let project_id: u32 = project_id.into();
    let project_id = base32::encode(
        base32::Alphabet::Rfc4648Lower { padding: false },
        &project_id.to_le_bytes(),
    );
    assert!(project_id.len() == 7);

    Ok(format!("{}-{}-{}", name.as_ref(), org_id, project_id))
}

pub fn decode(value: impl Into<String>) -> anyhow::Result<(String, OrgId, ProjectId)> {
    let mut value: String = value.into();

    if value.len() < 17 {
        return Err(anyhow::anyhow!("invalid index slug"));
    }

    let mut parts = value.rsplit('-');

    let project_id = parts
        .next()
        .ok_or_else(|| anyhow::anyhow!("invalid index slug"))?;
    let project_id = base32::decode(
        base32::Alphabet::Rfc4648Lower { padding: false },
        &project_id,
    )
    .ok_or_else(|| anyhow::anyhow!("invalid project id"))?;
    let project_id = u32::from_le_bytes(
        project_id
            .try_into()
            .or_else(|_| anyhow::bail!("invalid project id"))?,
    );

    let org_id = parts
        .next()
        .ok_or_else(|| anyhow::anyhow!("invalid index slug"))?;
    let org_id = base32::decode(base32::Alphabet::Rfc4648Lower { padding: false }, &org_id)
        .ok_or_else(|| anyhow::anyhow!("invalid org id"))?;
    let org_id = u32::from_le_bytes(
        org_id
            .try_into()
            .or_else(|_| anyhow::bail!("invalid org id"))?,
    );

    value.truncate(value.len() - 16);

    Ok((value, org_id.into(), project_id.into()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roundtrip() {
        for i in 0..1000 {
            let name = format!("index-{}", i);
            let org_id = OrgId::new(rand::random());
            let project_id = ProjectId::new(rand::random());

            let slug = encode(name.as_str(), org_id, project_id).unwrap();
            let d = decode(slug).unwrap();

            assert_eq!(d.0, name);
            assert_eq!(d.1, org_id);
            assert_eq!(d.2, project_id);
        }
    }

    #[test]
    fn test_index_with_dashes() {
        let slug = encode("foo-bar", 0.into(), 123.into()).unwrap();

        let (index_name, org_id, project_id) = decode(slug).unwrap();

        assert_eq!(index_name, "foo-bar");
        assert_eq!(org_id, 0.into());
        assert_eq!(project_id, 123.into());
    }

    #[test]
    fn test_edge_cases() {
        let slug = encode("---", 0.into(), 123.into()).unwrap();
        assert_eq!(decode(slug).unwrap().0, "---");

        let slug = encode("a", 0.into(), 123.into()).unwrap();
        assert_eq!(decode(slug).unwrap().0, "a");

        assert!(encode("", 0.into(), 123.into()).is_err());
        assert!(decode("-1-1").is_err());
    }

    #[test]
    fn test_malformed_slug() {
        assert!(decode("foo").is_err());
        assert!(decode("-").is_err());
        assert!(decode("--").is_err());
        assert!(decode("1").is_err());
        // > u64
        assert!(decode("foo-2345678909876543456789098765434567890987654323456789876543234567890876543456789876543245678909876543").is_err());
    }
}
