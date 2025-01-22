use genius_agent_factor_graph::test_util::generate_test_vfg_v0_4_0;
use genius_agent_factor_graph::FactorGraphStore;

fn main() {
    let graph = generate_test_vfg_v0_4_0();
    let db_path = format!("factor_graph_data/bench_{}", nanoid::nanoid!());
    let fg = FactorGraphStore::new(&db_path).unwrap();

    let options = microbench::Options::default();
    microbench::bench(&options, "validate_graph", || {
        fg.validate_graph(&graph).unwrap()
    });

    std::fs::remove_dir_all(db_path).unwrap()
}
