fn main() {
    let db_path = format!("factor_graph_data/bench_{}", nanoid::nanoid!());
    microbench::bench(&microbench::Options::default(), "open_speed", || {
        let fgs = FactorGraphStore::new(&db_path).unwrap();
        fgs.get_graph().unwrap();
    });
    let fgs = FactorGraphStore::new(&db_path).unwrap();
    microbench::bench(&microbench::Options::default(), "get_speed", || {
        fgs.get_graph().unwrap();
    });
}
