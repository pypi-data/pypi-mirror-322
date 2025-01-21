p1='''
is_valid_triangle <- function(a, b, c) {
  return((a + b > c) & (b + c > a) & (a + c > b))
}

triangle_type <- function(a, b, c) {
  if (a == b && b == c) {
    return("Equilateral")
  } else if (a == b || b == c || a == c) {
    return("Isosceles")
  } else {
    return("Scalene")
  }
}

triangle_area <- function(a, b, c) {
  s <- (a + b + c) / 2
  area <- sqrt(s * (s - a) * (s - b) * (s - c))
  return(area)
}

validate_input <- function(x) {
  if (!is.numeric(x) || x <= 0) {
    stop("Error: Input must be a positive number.")
  }
  return(TRUE)
}

cat("Enter the lengths of the sides of the triangle:\n")
a <- as.numeric(readline(prompt = "Side a: "))
b <- as.numeric(readline(prompt = "Side b: "))
c <- as.numeric(readline(prompt = "Side c: "))

tryCatch({
  validate_input(a)
  validate_input(b)
  validate_input(c)

  if (!is_valid_triangle(a, b, c)) {
    stop("Error: The given sides do not form a valid triangle.")
  }

  type_of_triangle <- triangle_type(a, b, c)
  cat("The triangle is:", type_of_triangle, "\n")

  area_of_triangle <- triangle_area(a, b, c)
  cat("The area of the triangle is:", area_of_triangle, "\n")

}, error = function(e) {
  cat(e$message, "\n")
})

'''

p2='''
set.seed(42)
random_vector <- runif(20, min = 1, max = 100)
cat("Original random vector:\n", random_vector, "\n")

sorted_vector <- sort(random_vector)
cat("Sorted vector:\n", sorted_vector, "\n")

search_value <- 50
is_value_present <- any(random_vector == search_value)
cat("Is", search_value, "present in the vector?", is_value_present, "\n")

values_greater_than_60 <- random_vector[random_vector > 60]
cat("Values greater than 60:\n", values_greater_than_60, "\n")

matrix_from_vector <- matrix(random_vector, nrow = 4, ncol = 5)
cat("Matrix from vector:\n")
print(matrix_from_vector)

matrix_transpose <- t(matrix_from_vector)
matrix_multiplication_result <- matrix_from_vector %*% matrix_transpose
cat("Matrix multiplication result:\n")
print(matrix_multiplication_result)

elementwise_multiplication_result <- matrix_from_vector * matrix_from_vector
cat("Element-wise matrix multiplication result:\n")
print(elementwise_multiplication_result)

my_list <- list(
  numbers = random_vector,
  characters = c("A", "B", "C", "D"),
  logical_values = c(TRUE, FALSE, TRUE),
  matrix = matrix_from_vector
)
cat("List:\n")
print(my_list)

subset_numeric <- my_list$numbers
cat("Subset (numeric part of the list):\n", subset_numeric, "\n")

subset_logical <- my_list$logical_values
cat("Subset (logical part of the list):\n", subset_logical, "\n")

my_list$characters[2] <- "Z"
cat("Modified list of characters:\n", my_list$characters, "\n")

squared_numbers <- my_list$numbers^2
cat("Squared numbers:\n", squared_numbers, "\n")

df <- data.frame(
  ID = 1:20,
  Age = sample(18:65, 20, replace = TRUE),
  Score = runif(20, min = 50, max = 100),
  Passed = sample(c(TRUE, FALSE), 20, replace = TRUE)
)
cat("Data frame:\n")
print(df)

filtered_df <- subset(df, Age > 30 & Score > 70)
cat("Filtered data frame (Age > 30 and Score > 70):\n")
print(filtered_df)

mean_age <- mean(df$Age)
sum_age <- sum(df$Age)
var_age <- var(df$Age)

mean_score <- mean(df$Score)
sum_score <- sum(df$Score)
var_score <- var(df$Score)

cat("Summary statistics for Age column:\n")
cat("Mean Age:", mean_age, "\n")
cat("Sum of Age:", sum_age, "\n")
cat("Variance of Age:", var_age, "\n")

cat("Summary statistics for Score column:\n")
cat("Mean Score:", mean_score, "\n")
cat("Sum of Score:", sum_score, "\n")
cat("Variance of Score:", var_score, "\n")

df$Score[sample(1:20, 5)] <- NA
cat("Data frame with missing values:\n")
print(df)

df$Score[is.na(df$Score)] <- mean(df$Score, na.rm = TRUE)
cat("Data frame after imputation of missing values:\n")
print(df)

library(dplyr)
grouped_stats <- df %>%
  group_by(Passed) %>%
  summarise(
    mean_score = mean(Score, na.rm = TRUE),
    mean_age = mean(Age)
  )
cat("Grouped statistics by Passed status:\n")
print(grouped_stats)
'''

p3='''
library(dplyr)
library(ggplot2)
library(moments)
library(palmerpenguins)

data(iris)
data(penguins)

calc_mode <- function(x) {
  return(as.numeric(names(sort(table(x), decreasing = TRUE)[1])))
}

print("----- Iris Dataset Analysis -----")
iris_mean <- sapply(iris[, 1:4], mean, na.rm = TRUE)
print(paste("Mean of Iris dataset:", iris_mean))

iris_median <- sapply(iris[, 1:4], median, na.rm = TRUE)
print(paste("Median of Iris dataset:", iris_median))

iris_mode <- sapply(iris[, 1:4], calc_mode)
print(paste("Mode of Iris dataset:", iris_mode))

iris_variance <- sapply(iris[, 1:4], var, na.rm = TRUE)
print(paste("Variance of Iris dataset:", iris_variance))

iris_sd <- sapply(iris[, 1:4], sd, na.rm = TRUE)
print(paste("Standard Deviation of Iris dataset:", iris_sd))

iris_skewness <- sapply(iris[, 1:4], skewness, na.rm = TRUE)
print(paste("Skewness of Iris dataset:", iris_skewness))

iris_kurtosis <- sapply(iris[, 1:4], kurtosis, na.rm = TRUE)
print(paste("Kurtosis of Iris dataset:", iris_kurtosis))

setosa <- subset(iris, Species == "setosa")$Sepal.Length
versicolor <- subset(iris, Species == "versicolor")$Sepal.Length
t_test <- t.test(setosa, versicolor)
print(t_test)

ggplot(iris, aes(x = Sepal.Length)) +
  geom_histogram(binwidth = 0.3, fill = "blue", color = "black") +
  ggtitle("Histogram of Sepal Length in Iris Dataset")

ggplot(iris, aes(x = Species, y = Sepal.Length, fill = Species)) +
  geom_boxplot() +
  ggtitle("Boxplot of Sepal Length by Species in Iris Dataset")

print("----- Palmer Penguins Dataset Analysis -----")
penguins_clean <- na.omit(penguins)

penguins_mean <- sapply(penguins_clean[, 3:6], mean, na.rm = TRUE)
print(paste("Mean of Palmer Penguins dataset:", penguins_mean))

penguins_median <- sapply(penguins_clean[, 3:6], median, na.rm = TRUE)
print(paste("Median of Palmer Penguins dataset:", penguins_median))

penguins_mode <- sapply(penguins_clean[, 3:6], calc_mode)
print(paste("Mode of Palmer Penguins dataset:", penguins_mode))

penguins_variance <- sapply(penguins_clean[, 3:6], var, na.rm = TRUE)
print(paste("Variance of Palmer Penguins dataset:", penguins_variance))

penguins_sd <- sapply(penguins_clean[, 3:6], sd, na.rm = TRUE)
print(paste("Standard Deviation of Palmer Penguins dataset:", penguins_sd))

penguins_skewness <- sapply(penguins_clean[, 3:6], skewness, na.rm = TRUE)
print(paste("Skewness of Palmer Penguins dataset:", penguins_skewness))

penguins_kurtosis <- sapply(penguins_clean[, 3:6], kurtosis, na.rm = TRUE)
print(paste("Kurtosis of Palmer Penguins dataset:", penguins_kurtosis))

adelie <- subset(penguins_clean, species == "Adelie")$flipper_length_mm
gentoo <- subset(penguins_clean, species == "Gentoo")$flipper_length_mm
t_test_penguins <- t.test(adelie, gentoo)
print(t_test_penguins)

ggplot(penguins_clean, aes(x = flipper_length_mm)) +
  geom_histogram(binwidth = 3, fill = "green", color = "black") +
  ggtitle("Histogram of Flipper Length in Palmer Penguins Dataset")

ggplot(penguins_clean, aes(x = species, y = flipper_length_mm, fill = species)) +
  geom_boxplot() +
  ggtitle("Boxplot of Flipper Length by Species in Palmer Penguins Dataset")
'''

p4='''

library(tidyverse)
library(titanic)
library(dplyr)
library(caret)
library(ggcorrplot)

data <- titanic::titanic_train

data$Age[is.na(data$Age)] <- median(data$Age, na.rm = TRUE)

mode_embarked <- as.character(names(sort(table(data$Embarked), decreasing = TRUE)[1]))
data$Embarked[is.na(data$Embarked)] <- mode_embarked

numeric_columns <- sapply(data, is.numeric)

z_scores <- as.data.frame(scale(data[, numeric_columns]))

outlier_condition <- apply(z_scores, 1, function(row) any(abs(row) > 3))

data_clean <- data[!outlier_condition, ]

summary_before <- summary(titanic::titanic_train)
summary_after <- summary(data_clean)

correlation_matrix <- cor(data_clean[, numeric_columns], use = "complete.obs")

write.csv(data_clean, "cleaned_titanic_data.csv", row.names = FALSE)

print("Summary Before Cleaning:")
print(summary_before)

print("Summary After Cleaning:")
print(summary_after)

print("Correlation Matrix:")
print(correlation_matrix)

ggcorrplot(correlation_matrix, method = "circle", lab = TRUE, title = "Correlation Matrix of Titanic Dataset")

data <- read.csv("C:/Users/kalya/Music/Tutorial Workshop Amulya/adult/adult.data", header = FALSE)

colnames(data) <- c('age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'income')

data[data == '?'] <- NA

replace_mode <- function(x) {
  mode_value <- as.character(names(sort(table(x), decreasing = TRUE)[1]))
  x[is.na(x)] <- mode_value
  return(x)
}

data <- data %>%
  mutate_if(is.character, replace_mode)

data <- data %>%
  mutate_if(is.numeric, ~ ifelse(is.na(.), median(., na.rm = TRUE), .))

remove_outliers <- function(x) {
  z_scores <- scale(x)
  x[abs(z_scores) <= 3]
}

numeric_columns <- sapply(data, is.numeric)

data_clean <- data %>%
  filter(!apply(as.data.frame(scale(data[, numeric_columns])), 1, function(row) any(abs(row) > 3)))

summary_before <- summary(read.csv("C:/Users/kalya/Music/Tutorial Workshop Amulya/adult/adult.data", header = FALSE))
summary_after <- summary(data_clean)

correlation_matrix <- cor(data_clean[, numeric_columns], use = "complete.obs")

write.csv(data_clean, "cleaned_adult_income_data.csv", row.names = FALSE)

print("Summary Before Cleaning:")
print(summary_before)

print("Summary After Cleaning:")
print(summary_after)

print("Correlation Matrix:")
print(correlation_matrix)

ggcorrplot(correlation_matrix, method = "circle", lab = TRUE, title = "Correlation Matrix of Adult Income Dataset")
'''

p5='''
library(dplyr)
library(nycflights13)
library(ggplot2)
library(zoo)

data("starwars")
head(starwars)

starwars_filtered <- starwars %>%
  select(name, species, height, mass) %>%
  filter(!is.na(species) & !is.na(height) & height > 100) %>%
  arrange(desc(height))

head(starwars_filtered)

ggplot(starwars_filtered, aes(x = reorder(name, -height), y = height, fill = species)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(title = "Height of Star Wars Characters", x = "Character", y = "Height (cm)") +
  theme_minimal()

species_summary <- starwars %>%
  group_by(species) %>%
  summarize(
    avg_height = mean(height, na.rm = TRUE),
    avg_mass = mean(mass, na.rm = TRUE),
    count = n()
  ) %>%
  arrange(desc(count))

head(species_summary)

ggplot(species_summary, aes(x = reorder(species, -avg_height), y = avg_height, fill = species)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(title = "Average Height by Species", x = "Species", y = "Average Height (cm)") +
  theme_minimal()

starwars_classified <- starwars %>%
  mutate(height_category = ifelse(height > 180, "Tall", "Short"))

head(starwars_classified)

ggplot(starwars_classified, aes(x = height_category, fill = height_category)) +
  geom_bar() +
  labs(title = "Distribution of Height Categories", x = "Height Category", y = "Count") +
  theme_minimal()

data("flights")
data("airlines")

flights_inner_join <- flights %>%
  inner_join(airlines, by = "carrier")

flights_outer_join <- flights %>%
  full_join(airlines, by = "carrier")

head(flights_inner_join)
head(flights_outer_join)

flights_rolling <- flights %>%
  arrange(year, month, day) %>%
  mutate(
    arr_delay = ifelse(is.na(arr_delay), 0, arr_delay),
    rolling_avg_delay = rollmean(arr_delay, 5, fill = NA),
    cumulative_delay = cumsum(arr_delay)
  )

head(flights_rolling)

ggplot(flights_rolling, aes(x = day)) +
  geom_line(aes(y = rolling_avg_delay, color = "Rolling Average Delay")) +
  geom_line(aes(y = cumulative_delay / 1000, color = "Cumulative Delay (x1000)")) +
  labs(title = "Rolling Average and Cumulative Delay of Flights", x = "Day of the Month", y = "Delay (minutes)") +
  scale_color_manual(values = c("Rolling Average Delay" = "blue", "Cumulative Delay (x1000)" = "red")) +
  theme_minimal()
'''

p6='''
library(ggplot2)
library(reshape2)
library(dplyr)

data("mpg")

ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, linetype = "dashed", color = "black", size = 1) +
  labs(title = "Scatter Plot of Engine Displacement vs Highway MPG with Regression Line",
       x = "Engine Displacement (L)",
       y = "Highway Miles per Gallon",
       color = "Vehicle Class") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
        axis.title = element_text(size = 14),
        legend.position = "bottom")

ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(color = "darkgreen", size = 2) +
  facet_wrap(~ class, ncol = 3) +
  labs(title = "Faceted Scatter Plot by Vehicle Class",
       x = "Engine Displacement (L)",
       y = "Highway Miles per Gallon") +
  theme_minimal() +
  theme(strip.text = element_text(size = 12, face = "italic"),
        plot.title = element_text(hjust = 0.5, size = 16))

data("diamonds")

cor_matrix <- cor(diamonds[, sapply(diamonds, is.numeric)], use = "complete.obs")
cor_data <- melt(cor_matrix)

ggplot(cor_data, aes(Var1, Var2, fill = value)) +
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = 0, limit = c(-1, 1), space = "Lab",
                       name = "Correlation") +
  labs(title = "Heatmap of Correlation Matrix for Diamonds Dataset",
       x = "Variables", y = "Variables") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        plot.title = element_text(hjust = 0.5, size = 16))

ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 3, shape = 21, fill = "lightblue", alpha = 0.8) +
  theme_light() +
  scale_color_brewer(palette = "Set2") +
  labs(title = "Customized Scatter Plot with Aesthetic Enhancements",
       x = "Engine Displacement (L)",
       y = "Highway Miles per Gallon",
       color = "Class") +
  theme(plot.title = element_text(face = "bold", size = 18),
        axis.title.x = element_text(size = 14),
        axis.title.y = element_text(size = 14),
        legend.background = element_rect(fill = "gray90"))

annotated_plot <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(color = "purple", size = 3) +
  annotate("text", x = 4, y = 40, label = "High Efficiency Zone",
           color = "red", size = 5, fontface = "bold", angle = 15) +
  annotate("rect", xmin = 2, xmax = 4, ymin = 30, ymax = 45,
           alpha = 0.2, fill = "yellow", color = "orange") +
  labs(title = "Annotated Scatter Plot with Highlighted Zone",
       x = "Engine Displacement (L)",
       y = "Highway Miles per Gallon") +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5))

ggsave("annotated_scatter_plot_expanded.png", annotated_plot, width = 10, height = 8, dpi = 300)

'''

p7='''
library(MASS)
library(ggplot2)
library(caret)
library(car)
library(pROC)
library(dplyr)
library(corrplot)

data("Boston")
head(Boston)

sum(is.na(Boston))
summary(Boston)

boxplot(Boston$medv, main = "Boxplot of Median Value of Homes (medv)")
Boston <- Boston %>% filter(medv < 50)

cor_matrix <- cor(Boston)
corrplot(cor_matrix, method = "circle")

simple_model <- lm(medv ~ lstat, data = Boston)
summary(simple_model)

multiple_model <- lm(medv ~ lstat * rm, data = Boston)
summary(multiple_model)

adjusted_R2 <- summary(multiple_model)$adj.r.squared
AIC_value <- AIC(multiple_model)
BIC_value <- BIC(multiple_model)

cat("Adjusted R^2:", adjusted_R2, "\n")
cat("AIC:", AIC_value, "\n")
cat("BIC:", BIC_value, "\n")

plot(multiple_model, which = 1, main = "Residuals vs Fitted Plot")
plot(multiple_model, which = 2, main = "Normal Q-Q Plot")

set.seed(123)
train_control <- trainControl(method = "cv", number = 10)
cv_model <- train(medv ~ lstat * rm, data = Boston, method = "lm", trControl = train_control)

print(cv_model)

Boston$medv_class <- ifelse(Boston$medv >= 25, 1, 0)
logistic_model <- glm(medv_class ~ lstat * rm, data = Boston, family = "binomial")
summary(logistic_model)

pred_probs <- predict(logistic_model, type = "response")
roc_curve <- roc(Boston$medv_class, pred_probs)

plot(roc_curve, main = "ROC Curve for Logistic Regression Model", col = "blue")
abline(a = 0, b = 1, lty = 2, col = "red")
cat("AUC:", auc(roc_curve), "\n")

'''
p8='''
library(rattle)
library(ggplot2)
library(cluster)
library(factoextra)
library(dplyr)

normalize <- function(data) {
  return((data - min(data)) / (max(data) - min(data)))
}

wine <- wine
wine_data <- wine[, -1]
wine_norm <- as.data.frame(lapply(wine_data, normalize))
wine_pca <- prcomp(wine_norm, scale. = TRUE)
summary(wine_pca)

wine_pca_data <- as.data.frame(wine_pca$x[, 1:2])
elbow_wine <- fviz_nbclust(wine_pca_data, kmeans, method = "wss")
print(elbow_wine)

silhouette_wine <- fviz_nbclust(wine_pca_data, kmeans, method = "silhouette")
print(silhouette_wine)

set.seed(123)
wine_kmeans <- kmeans(wine_pca_data, centers = 3, nstart = 25)
wine_pca_data$cluster <- as.factor(wine_kmeans$cluster)

p1 <- ggplot(wine_pca_data, aes(x = PC1, y = PC2, color = cluster)) +
  geom_point(size = 3) +
  labs(title = "k-means clustering on wine data set")
print(p1)

cat("Wine Dataset Clustering Results:\n")
cat("Clustering Sizes:", wine_kmeans$size, "\n")

library(readr)
bc_data <- read.csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data", header = FALSE)
bc_feature <- bc_data[, -c(1, 2)]
bc_norms <- as.data.frame(lapply(bc_feature, normalize))
bc_pca <- prcomp(bc_norms, scale. = TRUE)
summary(bc_pca)

bc_pca_data <- as.data.frame(bc_pca$x[, 1:2])
elbow_bc <- fviz_nbclust(bc_pca_data, kmeans, method = "wss")
print(elbow_bc)

silhouette_bc <- fviz_nbclust(bc_pca_data, kmeans, method = "silhouette")

set.seed(123)
bc_kmeans <- kmeans(bc_pca_data, centers = 2, nstart = 25)
bc_pca_data$cluster <- as.factor(bc_kmeans$cluster)

p2 <- ggplot(bc_pca_data, aes(x = PC1, y = PC2, color = cluster)) +
  geom_point(size = 3) +
  labs(title = "k-means clustering on breast cancer dataset")
print(p2)

cat("Breast Cancer Dataset Clustering Results:\n")
cat("Clustering Sizes:", bc_kmeans$size, "\n")
'''
p9='''
library(forecast)
library(ggplot2)
library(TSA)
library(tseries)

perform_eda <- function(ts_data, dataset_name) {
  cat("Exploratory Data Analysis for", dataset_name, "\n")
  print(summary(ts_data))
  plot(ts_data, main = paste(dataset_name, "Time Series"), ylab = "Values", xlab = "Time")
  cat("ACF and PACF plots:\n")
  acf(ts_data, main = paste("ACF of", dataset_name))
  pacf(ts_data, main = paste("PACF of", dataset_name))
}

decompose_ts <- function(ts_data, dataset_name) {
  cat("Decomposing the time series for", dataset_name, "\n")
  decomposition <- decompose(ts_data)
  plot(decomposition)
  return(decomposition)
}

fit_arima <- function(ts_data, dataset_name) {
  cat("Fitting ARIMA model for", dataset_name, "\n")
  adf_test <- adf.test(ts_data, alternative = "stationary")
  cat("ADF Test p-value:", adf_test$p.value, "\n")
  
  if (adf_test$p.value > 0.05) {
    ts_data <- diff(ts_data)
    plot(ts_data, main = paste(dataset_name, "Differenced Time Series"))
  }
  
  auto_model <- auto.arima(ts_data, seasonal = FALSE)
  print(summary(auto_model))
  forecast_result <- forecast(auto_model, h = 12)
  plot(forecast_result, main = paste(dataset_name, "ARIMA Forecast"))
  return(auto_model)
}

fit_sarima <- function(ts_data, dataset_name) {
  cat("Fitting SARIMA model for", dataset_name, "\n")
  auto_sarima <- auto.arima(ts_data, seasonal = TRUE)
  print(summary(auto_sarima))
  sarima_forecast <- forecast(auto_sarima, h = 12)
  plot(sarima_forecast, main = paste(dataset_name, "SARIMA Forecast"))
  return(auto_sarima)
}

compare_models <- function(arima_model, sarima_model, ts_data) {
  cat("Comparing ARIMA and SARIMA models:\n")
  h <- min(12, length(ts_data))
  arima_forecast <- forecast(arima_model, h = h)
  sarima_forecast <- forecast(sarima_model, h = h)
  actual_values <- ts_data[(length(ts_data) - h + 1):length(ts_data)]
  
  arima_accuracy <- accuracy(arima_forecast$mean, actual_values)
  sarima_accuracy <- accuracy(sarima_forecast$mean, actual_values)
  
  cat("ARIMA Forecast Accuracy:\n", arima_accuracy)
  cat("SARIMA Forecast Accuracy:\n", sarima_accuracy)
}

plot_forecast_comparison <- function(actual_values, arima_forecast, sarima_forecast, time_points) {
  arima_rmse <- sqrt(mean((arima_forecast - actual_values)^2))
  sarima_rmse <- sqrt(mean((sarima_forecast - actual_values)^2))
  
  better_color <- ifelse(arima_rmse < sarima_rmse, "green", "red")
  worse_color <- ifelse(arima_rmse < sarima_rmse, "red", "green")
  
  plot(time_points, actual_values, type = "o", col = "blue", pch = 16, lty = 1, xlab = "Time", ylab = "Values", main = "Forecast Comparison")
  lines(time_points, arima_forecast, col = better_color, lty = 2, lwd = 2)
  lines(time_points, sarima_forecast, col = worse_color, lty = 3, lwd = 2)
  
  legend("topright", legend = c("Actual Values", paste("ARIMA (RMSE =", round(arima_rmse, 2), ")"), paste("SARIMA (RMSE =", round(sarima_rmse, 2), ")")),
         col = c("blue", better_color, worse_color), lty = c(1, 2, 3), lwd = c(1, 2, 2), pch = c(16, NA, NA))
}

data("AirPassengers")
air_data <- AirPassengers
cat("\n- - - AirPassengers Dataset - - -\n")
perform_eda(air_data, "AirPassengers")
decompose_ts(air_data, "AirPassengers")
arima_air <- fit_arima(air_data, "AirPassengers")
sarima_air <- fit_sarima(air_data, "AirPassengers")
compare_models(arima_air, sarima_air, air_data)

h_air <- 12
air_actual_values <- air_data[(length (air_data) - h_air + 1):length(air_data)]
arima_air_forecast <- forecast(arima_air, h = h_air)$mean
sarima_air_forecast <- forecast(sarima_air, h = h_air)$mean
time_points_air <- time(air_data)[(length(air_data) - h_air + 1):length(air_data)]
plot_forecast_comparison(air_actual_values, arima_air_forecast, sarima_air_forecast, time_points_air)

data("milk")
milk_data <- milk
cat("\n- - - Monthly Milk Production Dataset - - -\n")
perform_eda(milk_data, "Monthly Milk Production")
decompose_ts(milk_data, "Monthly Milk Production")
arima_milk <- fit_arima(milk_data, "Monthly Milk Production")
sarima_milk <- fit_sarima(milk_data, "Monthly Milk Production")
compare_models(arima_milk, sarima_milk, milk_data)

h_milk <- 12
milk_actual_values <- milk_data[(length(milk_data) - h_milk + 1):length(milk_data)]
arima_milk_forecast <- forecast(arima_milk, h = h_milk)$mean
sarima_milk_forecast <- forecast(sarima_milk, h = h_milk)$mean
time_points_milk <- time(milk_data)[(length(milk_data) - h_milk + 1):length(milk_data)]
plot_forecast_comparison(milk_actual_values, arima_milk_forecast, sarima_milk_forecast, time_points_milk)
'''
p10='''
library(plotly)
library(gapminder)
library(dplyr)
data("gapminder")
scatter_plot <- gapminder %>%
  plot_ly(x = ~gdpPercap, y = ~lifeExp, color = ~continent,
          size = ~pop, hoverinfo = 'text', 
          text = ~paste("Country:", country, "<br>GDP per Capita:", gdpPercap),
          type = 'scatter', mode = 'markers') %>%
  layout(title = 'GDP vs Life Expectancy by Continent')
scatter_plot

bar_chart <- gapminder %>%
  filter(year == 2007) %>%
  plot_ly(x = ~country, y = ~lifeExp, type = 'bar',
          hoverinfo = 'text', 
          text = ~paste("Country:", country, "<br>Life Expectancy:", lifeExp)) %>%
  layout(title = 'Life Expectancy by Country in 2007')
bar_chart

line_chart <- gapminder %>%
  filter(continent == 'Asia') %>%
  plot_ly(x = ~year, y = ~lifeExp, color = ~country, type = 'scatter', mode = 'lines') %>%
  layout(title = 'Life Expectancy Trend in Asia')
line_chart

dashboard <- subplot(scatter_plot, bar_chart, line_chart, nrows = 1) %>%
  layout(title = 'Gapminder Data Visualization')
dashboard
'''