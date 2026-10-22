# Synthetic biomedical statistical foundations lab: executable quality gates.
# Run from repository root: Rscript --vanilla 03_learning/tests/test_statistical_test_lab.R
source("03_learning/examples/statistical_test_lab.R")

rejects <- function(expr) {
  inherits(tryCatch({ force(expr); NULL }, error = identity), "error")
}
lab <- make_statistical_test_lab()
a <- analyse_statistical_test_lab(lab)

stopifnot(
  identical(nrow(lab), 16L),
  identical(a$n_people, 16L),
  identical(unname(as.integer(a$group_counts)), c(8L, 8L)),
  identical(levels(lab$severity), c("I", "II", "III", "IV")),
  is.ordered(lab$severity),
  is.factor(lab$diagnosis),
  identical(unname(as.integer(a$contingency_counts)),
            c(4L, 3L, 4L, 5L)),
  isTRUE(all.equal(a$comparison_minus_reference, 3.875)),
  isTRUE(all.equal(a$paired_mean_change, 27 / 16)),
  isTRUE(all.equal(unname(a$paired$estimate), 27 / 16)),
  isTRUE(all.equal(unname(a$welch$estimate[2] - a$welch$estimate[1]),
                   3.875)),
  identical(a$welch$method, "Welch Two Sample t-test"),
  a$welch$p.value >= 0, a$welch$p.value <= 1,
  a$paired$p.value >= 0, a$paired$p.value <= 1,
  a$fisher$p.value >= 0, a$fisher$p.value <= 1,
  is.finite(unname(a$correlation$estimate)),
  all(is.finite(coef(a$logistic))),
  all(is.finite(coef(a$poisson_rate))),
  a$poisson_rate$family$family == "poisson"
)
# A row permutation preserves group structure and matched within-row changes.
reordered <- analyse_statistical_test_lab(lab[rev(seq_len(nrow(lab))), ,
                                              drop = FALSE])
stopifnot(
  isTRUE(all.equal(reordered$comparison_minus_reference,
                   a$comparison_minus_reference)),
  isTRUE(all.equal(reordered$paired_mean_change,
                   a$paired_mean_change)),
  isTRUE(all.equal(reordered$fisher$p.value, a$fisher$p.value))
)
# Reject invalid structure, missing and biologically misleading inputs.
bad <- lab
bad$person_id[2] <- bad$person_id[1]
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$exposure_years[1] <- 0
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$event_count[1] <- -1L
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$event_count[1] <- 0.5
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$group[1] <- NA
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$severity <- as.character(bad$severity)
stopifnot(rejects(analyse_statistical_test_lab(bad)))

bad <- lab
bad$after_au[1] <- NA_real_
stopifnot(rejects(analyse_statistical_test_lab(bad)))

cat("PASS: synthetic data-type and test lab; numeric fixtures, group/pair alignment, inference contracts and invalid inputs\n")
