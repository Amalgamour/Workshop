//! Page 90.50.10.0416. The five Windows fixes stay in tests/wf.rs.

#[test]
fn the_five_windows_tests_stay_in_wf_rs() {
    let src = include_str!("wf.rs");
    for name in [
        "check_stores_at_most_last_40_lines_of_output",
        "check_escapes_ansi_cursor_codes_so_a_fail_cannot_repaint_the_screen",
        "return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii",
        "planted_file_names_are_escaped_in_views",
        "board_escapes_hostile_log_text_everywhere",
    ] {
        assert!(src.contains(&format!("fn {name}(")), "{name} is missing from tests/wf.rs");
    }
}
