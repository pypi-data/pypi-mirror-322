// re-export protos for in-macro use
pub use topk_protos as protos;

#[macro_export]
macro_rules! doc {
    ($($field:expr => $value:expr),* $(,)?) => {
        topk_sdk_core::macros::protos::v1::data::Document::from([
            $(($field, $value.into())),*
        ])
    };
}

#[macro_export]
macro_rules! schema {
    () => {
        topk_sdk_core::macros::protos::v1::control::index_schema::IndexSchema::default()
    };
    ($($field:expr => $spec:expr),* $(,)?) => {{
        let schema = topk_sdk_core::macros::protos::v1::control::index_schema::IndexSchema::try_from([
            $(($field, $spec)),*
        ]);

        schema.unwrap()
    }};
}
