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
d4 = format_data("D0400001.dat", "D0400001.csv", 4688582, 7)
d5 = format_data("D0600001.dat", "D0600001.csv", 5369767, 7)
d6 = format_data("D0800001.dat", "D0800001.csv", 5349176, 7)
d7 = format_data("V6_00001.dat", "V6_00001.csv", 5301441, 7)
d8 = format_data("V17_0001.dat", "V17_0001.csv", 5349176, 7)
d9 = format_data("V20_0001.dat", "V20_0001.csv", 5960281, 7)
d10 = format_data("V24_0001.dat", "V24_0001.csv", 5389292, 7)
d11 = format_data("V25a_001.dat", "V25a_001.csv", 5457655, 7)