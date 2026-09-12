// This is an example manifest. Copy it to manifest.js and edit the list
// to match the episodes you have prepared data files for.
//
// - id:      a unique string, used as the localStorage progress key
// - season:  used only to group the dropdown into "第 N 季" (Season N) headers
// - episode: not currently used by the UI beyond sorting within a season,
//            but keep it consistent with your file naming
// - title:   shown in the episode dropdown
// - file:    path (relative to index.html) to that episode's data file
window.SERIES_MANIFEST = [
  { id: "example-01", season: 1, episode: 1, title: "示例第1集 (Example Episode 1)", file: "data/example-episode.js" }
];
