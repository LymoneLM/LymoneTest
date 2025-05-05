library(igraph)
library(ggraph)
library(tidygraph)
library(dplyr)

bike_data <- read.csv("./data/LondonBikeJourneyAug2023.csv")

edges <- bike_data %>%
  group_by(Start.station.number, End.station.number) %>%
  summarise(weight = n(), .groups = "drop") %>%
  filter(weight > 10) # 过滤掉边的权重小于10的边，以减少图的复杂性，降低加算复杂性

net <- graph_from_data_frame(d = edges, directed = TRUE)


p1 <- ggraph(net, layout = "mds") +
  geom_edge_link(
    aes(
      edge_color = weight,
      edge_alpha = weight
    ),
    edge_width = 0.2
  ) +
  scale_edge_color_gradient(
    low = "#f55252",
    high = "#800000"
  ) +
  scale_edge_alpha(range = c(0.2, 0.8)) +
  geom_node_point(
    size = 0.5,
    color = "black",
    alpha = 0.8
  ) +
  labs(title = "伦敦自行车租赁站点网络图") +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 12, face = "bold"),
    legend.position = "bottom"
  )

ggsave("./output/4/bike_network_plot.png", p1, bg = "white", width = 10, height = 8, dpi = 300)
write.csv(edges, "./output/4/bike_network_edges.csv", row.names = FALSE)
