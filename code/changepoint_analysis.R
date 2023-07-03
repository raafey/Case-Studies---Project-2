setwd("C://Users//Raafe//Desktop//TU Dortmund//Semester 5//Case Studies//Case-Studies---Project-2")
data = read.csv("processed_dir/V2_00001_processed_data.csv", header = TRUE)
library(cpm)
fit_cpm = processStream(data$CH1_Moment, cpmType = "Student")
c1 = cpt.var(data$CH1_Moment)
plot(data$time, data$CH1_Moment, type="S")
abline(v = data$time[c1@cpts] , col = "red", lty = "dashed")

library(EnvCpt)
cpt_env = envcpt(data$CH1_Moment, models=c("trendcpt"))

library(changepoint)
