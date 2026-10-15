# Interactive companion to hse_specialist_visuals.R.
# Preserve the original ggplot2 object as the numerical/manuscript authority.
# Plotly HTML encodes underlying plot data: never publish patient-level values
# or identifiers without an explicit privacy, permissions and release review.

hse_plotly_view <- function(plot, tooltip = "all") {
  if (!inherits(plot, "ggplot"))
    stop("plot must be an existing ggplot object", call. = FALSE)
  if (!requireNamespace("plotly", quietly = TRUE))
    stop("The plotly R package is required for interactive output", call. = FALSE)
  if (!is.character(tooltip) || !length(tooltip) ||
      anyNA(tooltip) || any(!nzchar(tooltip)))
    stop("tooltip must be a nonempty character vector", call. = FALSE)

  # Conversion never changes the original plot or statistical calculations.
  widget <- plotly::ggplotly(plot, tooltip = tooltip)
  plotly::config(
    widget,
    displayModeBar = TRUE,
    displaylogo = FALSE,
    responsive = TRUE,
    scrollZoom = FALSE,
    toImageButtonOptions = list(format = "png", scale = 2)
  )
}

hse_save_plotly <- function(plot, file, tooltip = "all") {
  if (!is.character(file) || length(file) != 1L ||
      is.na(file) || !nzchar(trimws(file)) ||
      !grepl("\\.html$", file, ignore.case = TRUE))
    stop("file must name a nonempty .html destination", call. = FALSE)
  if (!requireNamespace("htmlwidgets", quietly = TRUE))
    stop("htmlwidgets is required for offline HTML export", call. = FALSE)

  widget <- if (inherits(plot, "plotly")) plot else
    hse_plotly_view(plot, tooltip = tooltip)
  dirname_file <- dirname(file)
  dir.create(dirname_file, showWarnings = FALSE, recursive = TRUE)
  dependency_name <- paste0(tools::file_path_sans_ext(basename(file)), "_files")
  htmlwidgets::saveWidget(widget, file, selfcontained = FALSE,
                          libdir = dependency_name,
                          title = "Interactive biomedical visualization")
  dependencies <- file.path(dirname_file, dependency_name)
  if (!file.exists(file) || !dir.exists(dependencies) ||
      !length(list.files(dependencies, recursive = TRUE)))
    stop("Interactive HTML or its local JavaScript dependencies are missing",
         call. = FALSE)
  invisible(list(html = normalizePath(file),
                 dependencies = normalizePath(dependencies)))
}
