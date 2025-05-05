library(igraph)
library(ggraph)
library(tidygraph)
library(dplyr)

bike_data <- read.csv("./data/LondonBikeJourneyAug2023.csv")

edges <- bike_data %>%
  group_by(Start.station.number, End.station.number) %>%
  summarise(weight = n(), .groups = "drop") %>%
  filter(weight > 30)  

net <- graph_from_data_frame(d = edges, directed = TRUE)

p1 <- ggraph(net, layout = "kk") +  
  geom_edge_link(aes(edge_width = weight / max(weight) * 2), alpha = 0.4, color = "#ce280b") +  
  geom_node_point(size = 1, color = "black") +  
  labs(title = "伦敦自行车租赁站点网络图") +
  theme_void()

ggsave("./output/4/bike_network_plot.png", p1, bg = "white", width = 10, height = 8, dpi = 300)
write.csv(edges, "./output/4/bike_network_edges.csv", row.names = FALSE)
