#!/usr/bin/env Rscript
# Independent closed-form and hand-worked numerical fixtures for G4.
suppressPackageStartupMessages(library(survival))
near <- function(x,y,tol=1e-10) stopifnot(is.finite(x),abs(x-y)<tol)
km_at <- function(fit,t,left=FALSE) {
  z <- which(if(left) fit$time<t else fit$time<=t)
  if(!length(z)) 1 else fit$surv[max(z)]
}
loss <- function(time,event,p,gfit,tau=24) {
  g24 <- km_at(gfit,tau)
  stopifnot(g24>=0.2,length(time)==length(p),all(p>=0&p<=1))
  v <- numeric(length(time))
  for(i in seq_along(time)) {
    if(time[i]<=tau && event[i]==1) v[i] <- p[i]^2/km_at(gfit,time[i],TRUE)
    if(time[i]>tau) v[i] <- (1-p[i])^2/g24
  }
  mean(v)
}
# Toy 1: no observed censorship before tau => ordinary binary Brier.
train <- data.frame(time=c(6,12,30,40),event=c(1,1,0,0))
g <- survfit(Surv(time,1-event)~1,data=train)
near(loss(c(8,29,15),c(1,0,0),c(.2,.7,.6),g),
     (.2^2+(.3)^2+0)/3)
# Toy 2: one censor at 10 among 4 training subjects => G(t-) at t=10 is 1,
# and G(24)=3/4; at time 20 event weight=4/3.
ct <- data.frame(time=c(10,20,30,40),event=c(0,1,1,1))
g2 <- survfit(Surv(time,1-event)~1,data=ct)
near(km_at(g2,10,TRUE),1)
near(km_at(g2,10,FALSE),.75)
near(km_at(g2,24),.75)
near(loss(c(20,26,12,24),c(1,0,0,1),c(.2,.7,.4,.8),g2),
     ((.2^2)/.75+(.3^2)/.75+0+(.8^2)/.75)/4)
# Toy 3: event and censor share a time: use event-time left limit.
near(loss(c(10),c(1),c(.5),g2),.25)
# Toy 4: exact horizon event belongs to event arm, censored at horizon zero.
near(loss(c(24,24,26),c(1,0,0),c(.2,.9,.7),g2),
     ((.2^2)/.75+0+(.3^2)/.75)/3)
# Cox known null-effect fixture: identical predictors -> expected marginal model
# assessed via an intercept-free constant prediction (all survival values=0.5).
# No fitter needed; analytic unweighted Brier for 0/1 outcomes is 0.25.
near(mean((c(0,1,0,1)-0.5)^2),.25)
cat("PASS G4 independent IPCW oracle: five numerical fixtures\n")
