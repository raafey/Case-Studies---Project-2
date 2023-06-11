format_data = function(dat_file_path, csv_name, num_samples, num_series) {
 
  n = num_samples * num_series
  data = readBin(dat_file_path, what="integer", size=2, endian="little", signed=TRUE, n=n)
  data = matrix(data, nrow=num_series)
  data = t(data)
  data = as.data.frame(data)
  write.csv(data, csv_name, row.names=FALSE)
  
  return (data)
}


d1 = format_data("V2_00001-1.DAT", "V2_00001-1.csv", 5829936, 1)
d2 = format_data("V2_00001.dat", "V2_00001.csv", 5829936, 7)
d3 = format_data("V10_0001.dat", "V10_0001.csv", 5290814, 7)
