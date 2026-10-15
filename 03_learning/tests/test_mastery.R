# Competency checks on fresh synthetic inputs. No source-course files are required.
source("03_learning/examples/research_case.R")
source("03_learning/examples/practice_tools.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
passed <- character()
check <- function(id, expr) {
  if (!isTRUE(force(expr))) stop(paste("Learning check failed:", id), call. = FALSE)
  passed <<- c(passed, id)
}
workspace <- tempfile("mastery-")
dir.create(workspace)

check("LC01", 3 + 4 * 2 == 11 && (3 + 4) * 2 == 14 && 17 %/% 5 == 3 && 17 %% 5 == 2)
v <- setNames(c(3, 7, 11), c("A", "B", "C"))
check("LC02", identical(unname(checked_offsets(v, 2)), c(5, 9, 13)) &&
  rejects(checked_offsets(v, c(1, 2))))
x <- c(4, NA_real_, NaN, Inf, 8)
flag <- rep(NA, length(x)); flag[is.finite(x)] <- x[is.finite(x)] > 6
check("LC03", sum(is.na(x)) == 2 && sum(is.nan(x)) == 1 && sum(is.finite(x)) == 2 &&
  length(NULL) == 0 && mean(x[is.finite(x)]) == 6 && identical(flag, c(FALSE, NA, NA, NA, TRUE)))
record <- list(values = matrix(1:6, nrow = 2), units = "invented au")
check("LC04", is.list(record["values"]) && is.matrix(record[["values"]]) &&
  identical(dim(record$values[1, , drop = FALSE]), c(1L, 3L)) &&
  identical(unname(v[c("C", "A")]), c(11, 3)))
f <- clean_panel(c(" BETA ", "alpha", "Beta"))
check("LC05", identical(levels(f), c("alpha", "beta")) && identical(as.integer(f), c(2L, 1L, 2L)) &&
  rejects(clean_panel(c("alpha", "gamma"))) &&
  as.numeric(as.Date("2032-03-12") - as.Date("2032-03-02")) == 10)
m <- matrix(c(2, 6, 4, 8), nrow = 2)
check("LC06", identical(unname(rowMeans(m)), c(3, 7)) &&
  identical(unname(colMeans(m)), c(4, 6)) && isTRUE(all.equal(m %*% diag(2), m)))
loop_result <- numeric(length(v))
for (i in seq_along(v)) loop_result[i] <- v[i] * 2
cursor <- 1L
while (cursor <= length(v)) {stopifnot(loop_result[cursor] == 2 * v[cursor]); cursor <- cursor + 1L}
check("LC07", identical(loop_result, unname(vapply(v, function(z) z * 2, numeric(1)))) &&
  is.list(lapply(v, sqrt)) && rejects(assert(c(TRUE, FALSE), "scalar required")) &&
  rejects(assert(NA, "missing decision")))
small <- data.frame(code = c("001", "002"), panel = factor(c("alpha", "beta"),
  levels = c("alpha", "beta", "unused")), measurement = c(5, NA_real_))
write.csv(small, file.path(workspace, "records.csv"), row.names = FALSE, na = "NA")
restored <- read.csv(file.path(workspace, "records.csv"),
  colClasses = c("character", "character", "numeric"), na.strings = "NA")
saveRDS(small, file.path(workspace, "records.rds"))
check("LC08", identical(restored$code, small$code) && identical(restored$measurement, small$measurement) &&
  is.character(restored$panel) && identical(readRDS(file.path(workspace, "records.rds")), small))
case <- make_case(); result <- analyse_case(case)
check("LC09", identical(result$ledger$n, c(8L, 16L, 14L, 6L, 7L)))
check("LC10", identical(as.integer(table(clean_panel(c(" alpha ", "BETA", "Alpha")))), c(2L, 1L)))
responses <- decode_response(c("Y", "N", "R", "U", NA_character_))
check("LC11", identical(as.character(responses), c("reported_yes", "reported_no", "refused", "uncertain", NA_character_)) &&
  rejects(decode_response("diagnosed")))
for (package in c("dplyr", "tidyr", "ggplot2", "survey")) {
  if (!requireNamespace(package, quietly = TRUE)) stop(paste("Mastery checks require", package))
}
stopifnot(utils::packageVersion("dplyr") >= "1.1.0")
people <- data.frame(id = c("J1", "J2", "J3", "J4"), age = c(21, 32, 43, 54))
assays <- data.frame(id = c("J2", "J4", "J5"), value = c(6, 8, 10))
left <- dplyr::left_join(people, assays, by = "id", relationship = "one-to-one")
inner <- dplyr::inner_join(people, assays, by = "id", relationship = "one-to-one")
full <- dplyr::full_join(people, assays, by = "id", relationship = "one-to-one")
repeats <- data.frame(id = c("J1", "J1", "J2"), day = c(0, 9, 0))
check("LC12", nrow(left) == 4L && nrow(inner) == 2L && nrow(full) == 5L &&
  nrow(dplyr::anti_join(people, assays, by = "id")) == 2L &&
  nrow(dplyr::anti_join(assays, people, by = "id")) == 1L &&
  nrow(dplyr::left_join(repeats, people, by = "id", relationship = "many-to-one")) == 3L &&
  nrow(dplyr::left_join(people, repeats, by = "id", relationship = "one-to-many")) == 5L &&
  rejects(dplyr::left_join(repeats, rbind(people, people[1, ]), by = "id", relationship = "many-to-one")))
long <- case$visits[c("person_id", "visit", "marker_au")]
wide <- tidyr::pivot_wider(long, names_from = "visit", values_from = "marker_au")
back <- tidyr::pivot_longer(wide, cols = c("baseline", "followup"), names_to = "visit", values_to = "marker_au")
sort_rows <- function(d) {d <- as.data.frame(d); d <- d[order(d$person_id, d$visit), ]; rownames(d) <- NULL; d}
check("LC13", identical(sort_rows(long), sort_rows(back)))
modified <- dplyr::mutate(case$registry, panel_clean = clean_panel(rep(c(" ALPHA", "Beta "), 4)),
  selected = age_years >= 34)
selected <- dplyr::arrange(dplyr::select(dplyr::filter(modified, selected), person_id, age_years), age_years)
groups <- dplyr::summarise(dplyr::group_by(modified, panel_clean), n_people = dplyr::n(), .groups = "drop")
check("LC14", nrow(selected) == 6L && sum(groups$n_people) == 8L &&
  identical(groups$n_people, c(4L, 4L)))
visit_groups <- dplyr::summarise(dplyr::group_by(result$joined, arm),
  n_people = dplyr::n_distinct(person_id), n_visits = dplyr::n(), .groups = "drop")
stopifnot(sum(visit_groups$n_people) == 8L, sum(visit_groups$n_visits) == 16L)
check("LC15", nrow(result$pairs) == 6L && mean(result$pairs$change_au) == 1.5 &&
  sum(result$summary$n_observed) == 14L)
# Software mechanics on deliberately chosen differences, not a clinical test claim.
changes <- c(-2, 1, 4, 6, 9)
rank <- wilcox.test(changes, mu = 0, exact = TRUE)
test <- t.test(changes, mu = 0)
check("LC16", unname(rank$statistic) == 13 && is.finite(rank$p.value) &&
  isTRUE(all.equal(unname(test$statistic), mean(changes) / (sd(changes) / sqrt(length(changes))))))
set.seed(418)
draws <- list(normal = rnorm(40), uniform = runif(40, -2, 3), binary = rbinom(40, 1, .3))
set.seed(418)
again <- list(normal = rnorm(40), uniform = runif(40, -2, 3), binary = rbinom(40, 1, .3))
check("LC17", identical(draws, again) && all(draws$uniform >= -2 & draws$uniform <= 3) &&
  all(draws$binary %in% 0:1))
# Comparable numerical slopes can conceal nonlinearity and influential points.
slopes <- vapply(seq_len(4), function(i) unname(coef(lm(
  datasets::anscombe[[paste0("y", i)]] ~ datasets::anscombe[[paste0("x", i)]]))[2]), numeric(1))
check("LC18", diff(range(slopes)) < 0.01 &&
  length(unique(datasets::anscombe$x4)) < length(unique(datasets::anscombe$x1)))
check("LC19", nobs(result$model) == 7L && "S02" %in% result$model_data$person_id &&
  is.finite(coef(result$model)[["age_years"]]))
check("LC20", all((result$prediction$upr - result$prediction$lwr) >
  (result$confidence$upr - result$confidence$lwr)))
check("LC21", length(residuals(result$model)) == 7L && length(fitted(result$model)) == 7L)
plotted <- checked_scatter(data.frame(age = c(20, NA, 40, 50), signal = c(2, 3, 4, Inf)),
  "age", "signal", "years", "au", draw = FALSE)
check("LC22", plotted$n_total == 4L && plotted$n_eligible == 2L && plotted$n_excluded == 2L &&
  rejects(checked_scatter(data.frame(x = "bad", y = 1), "x", "y", "years", "au", draw = FALSE)) &&
  rejects(checked_scatter(data.frame(x = 1, y = 2), "x", "y", "", "au", draw = FALSE)))
figure <- file.path(workspace, "distribution_checks.pdf")
pdf(figure, width = 8, height = 6)
par(mfrow = c(2, 2))
for (i in seq_len(4)) {
  plot(datasets::anscombe[[paste0("x", i)]], datasets::anscombe[[paste0("y", i)]],
    xlab = "Example x", ylab = "Example y", main = paste("Summary contrast", i))
}
par(mfrow = c(2, 2))
x <- c(2, 4, 5, 8, 9, 11)
hist(x, xlab = "Synthetic marker (au)", main = "Six measurements")
plot(density(x), xlab = "Synthetic marker (au)", main = "Density; not record count")
plot(ecdf(x), xlab = "Synthetic marker (au)", ylab = "Observed fraction", main = "Empirical distribution")
boxplot(x, ylab = "Synthetic marker (au)", main = "Quantile summary")
frame <- data.frame(panel = rep(c("A", "B"), each = 3), value = x)
violin <- ggplot2::ggplot(frame, ggplot2::aes(x = panel, y = value)) +
  ggplot2::geom_violin() + ggplot2::geom_boxplot(width = .15) + ggplot2::geom_point() +
  ggplot2::labs(x = "Invented panel", y = "Marker (invented au)", caption = "Three synthetic measurements per panel")
print(violin)
dev.off()
check("LC23", file.info(figure)$size > 0 && inherits(violin, "ggplot") &&
  ecdf(x)(5) == .5 && violin$labels$y == "Marker (invented au)")
one_value <- matrix(c(1, NA_real_, NA_real_), nrow = 1)
check("LC24", identical(scale_features(one_value)$status, "insufficient_observations") &&
  all(result$scaled$values["DemoConstant", ] == 0) &&
  all(is.na(result$scaled$values["DemoMissing", ])))
sample <- data.frame(cluster = rep(1:4, each = 2), stratum = rep(c("A", "B"), each = 4),
  weight = c(1, 1, 2, 2, 1, 1, 2, 2), marker = c(1, 3, 5, 7, 9, 11, 13, 15))
design <- survey::svydesign(ids = ~cluster, strata = ~stratum, weights = ~weight, data = sample)
estimate <- survey::svymean(~marker, design)
check("LC25", isTRUE(all.equal(as.numeric(coef(estimate)), weighted.mean(sample$marker, sample$weight))) &&
  is.finite(as.numeric(survey::SE(estimate))) && weighted.mean(sample$marker, sample$weight) != mean(sample$marker))
unlink(workspace, recursive = TRUE)
stopifnot(length(unique(passed)) == 25L)
cat(sprintf("PASS: %d executable competency groups, including optional-package operations and figure exports\n", length(passed)))
