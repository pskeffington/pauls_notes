# CO-06: base R counterpart to synthetic calculus and least-squares lab.
# Independent reference implementation; no participant data or clinical use.

checked <- function(x, label) {
  if (!is.numeric(x) || is.logical(x) || length(x) < 1L ||
      any(!is.finite(x))) stop(paste(label, "must be finite numeric"), call.=FALSE)
  as.numeric(x)
}
paired <- function(x,y,min_n=2L) {
  a <- checked(x,"x"); b <- checked(y,"y")
  if (length(a)!=length(b) || length(a)<min_n)
    stop("paired observations require matching lengths",call.=FALSE)
  list(a,b)
}
average_slope <- function(t0,y0,t1,y1) {
  t0 <- checked(t0,"t0"); y0<-checked(y0,"y0")
  t1 <- checked(t1,"t1"); y1<-checked(y1,"y1")
  if (any(lengths(list(t0,y0,t1,y1))!=1) || t1<=t0)
    stop("invalid time points",call.=FALSE)
  (y1-y0)/(t1-t0)
}
dot <- function(a,b) {
  p<-paired(a,b,1L)
  sum(p[[1]]*p[[2]])
}
matrix_vector <- function(X, beta) {
  if (!is.matrix(X) || !is.numeric(X) || any(!is.finite(X)))
    stop("X must be finite numeric matrix",call.=FALSE)
  b<-checked(beta,"beta")
  if (ncol(X)!=length(b) || nrow(X)<1L)
    stop("incompatible matrix dimensions",call.=FALSE)
  drop(X %*% b)
}
ols_line <- function(x,y) {
  p<-paired(x,y,3L); x<-p[[1]]; y<-p[[2]]
  X<-cbind(intercept=1, marker=x)
  if (qr(X)$rank !=2L) stop("rank deficient design",call.=FALSE)
  beta<-drop(qr.solve(X,y))
  setNames(beta,c("intercept","slope"))
}
half_mse <- function(x,y,beta) {
  p<-paired(x,y)
  b<-checked(beta,"beta")
  if(length(b)!=2L) stop("intercept and slope required",call.=FALSE)
  residuals <- b[1]+b[2]*p[[1]]-p[[2]]
  sum(residuals^2)/(2*length(residuals))
}
mse_gradient <- function(x,y,beta) {
  p<-paired(x,y); b<-checked(beta,"beta")
  if(length(b)!=2L) stop("intercept and slope required",call.=FALSE)
  residuals<-b[1]+b[2]*p[[1]]-p[[2]]
  c(mean(residuals), mean(residuals*p[[1]]))
}
numeric_gradient <- function(x,y,beta,h=1e-5) {
  b<-checked(beta,"beta"); h<-checked(h,"h")
  if(length(b)!=2L || length(h)!=1L || h<=0)
    stop("invalid finite difference settings",call.=FALSE)
  sapply(1:2,function(i) {
    plus<-b; minus<-b
    plus[i]<-plus[i]+h
    minus[i]<-minus[i]-h
    (half_mse(x,y,plus)-half_mse(x,y,minus))/(2*h)
  })
}
gradient_descent <- function(x,y,step=0.1,iterations=2000L) {
  p<-paired(x,y,3L); step<-checked(step,"step")
  if(length(step)!=1L || step<=0 || step>=0.2 ||
     length(iterations)!=1L || is.na(iterations) || !is.numeric(iterations) ||
     iterations!=floor(iterations) || iterations<1 || iterations>10000)
    stop("invalid teaching optimizer parameters",call.=FALSE)
  beta<-c(0,0)
  for(i in seq_len(iterations)) {
    beta<-beta-step*mse_gradient(p[[1]],p[[2]],beta)
    if(any(!is.finite(beta)))stop("optimizer diverged",call.=FALSE)
  }
  beta
}
trapezoid <- function(time, measurement) {
  p<-paired(time,measurement)
  t<-p[[1]]; y<-p[[2]]
  if(any(diff(t)<=0))stop("time must increase strictly",call.=FALSE)
  sum(diff(t)*(head(y,-1L)+tail(y,-1L))/2)
}
fixture <- function() {
  x<-c(0,1,2,3); y<-c(1,2,4,4)
  b<-ols_line(x,y)
  list(average_slope=average_slope(0,1,2,5),
       derivative_at_three=2*3,
       numeric_derivative=((3+1e-5)^2-(3-1e-5)^2)/(2e-5),
       dot_product=dot(c(1,2,3),c(4,5,6)),
       ols_coefficients=unname(b),
       fitted_values=matrix_vector(cbind(1,x),unname(b)),
       half_mse=half_mse(x,y,unname(b)),
       starting_gradient=mse_gradient(x,y,c(0,0)),
       numeric_gradient=numeric_gradient(x,y,c(0,0)),
       gradient_descent=gradient_descent(x,y),
       logistic_at_zero=plogis(0),
       logistic_derivative_at_zero=plogis(0)*(1-plogis(0)),
       trapezoidal_area=trapezoid(c(0,1,2),c(1,3,3)))
}
expect_error <- function(expr) {
  did_error<-tryCatch({ force(expr); FALSE },error=function(e) TRUE)
  if(!did_error)stop("invalid input was accepted",call.=FALSE)
}
if (sys.nframe()==0L) {
  a<-fixture()
  stopifnot(isTRUE(all.equal(a$average_slope,2)),
            isTRUE(all.equal(a$derivative_at_three,6)),
            isTRUE(all.equal(a$numeric_derivative,6,tolerance=1e-8)),
            isTRUE(all.equal(a$dot_product,32)),
            isTRUE(all.equal(a$ols_coefficients,c(1.1,1.1),tolerance=1e-10)),
            isTRUE(all.equal(a$fitted_values,c(1.1,2.2,3.3,4.4),tolerance=1e-10)),
            isTRUE(all.equal(a$half_mse,0.0875,tolerance=1e-10)),
            isTRUE(all.equal(a$starting_gradient,c(-2.75,-5.5))),
            isTRUE(all.equal(a$numeric_gradient,c(-2.75,-5.5),tolerance=1e-7)),
            isTRUE(all.equal(a$gradient_descent,c(1.1,1.1),tolerance=1e-6)),
            isTRUE(all.equal(a$logistic_at_zero,0.5)),
            isTRUE(all.equal(a$logistic_derivative_at_zero,0.25)),
            isTRUE(all.equal(a$trapezoidal_area,5)))
  expect_error(ols_line(c(1,1,1),c(1,2,3)))
  expect_error(average_slope(1,2,1,4))
  expect_error(dot(c(1,2),c(3)))
  expect_error(matrix_vector(matrix(1:4,2,2),c(1)))
  expect_error(gradient_descent(c(0,1,2),c(1,2,3),step=0))
  expect_error(trapezoid(c(0,1,1),c(1,2,3)))
  expect_error(half_mse(c(1,2),c(1,2),c(0,0,0)))
  print(a)
  cat("CO-06 R fixture and negative checks passed\n")
}
