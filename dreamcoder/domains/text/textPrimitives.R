isUpper <- function(x) {
    return(x == toupper(x))
}

increment <- function(x) {
    return(x + 1)
}

decrement <- function(x) {
    return(x - 1)
}

lower <- function(x) {
    return(tolower(x))
}

upper <- function(x) {
    return(toupper(x))
}

capitalize <- function(x) {
    substr(x, 1, 1) <- toupper(substr(x, 1, 1))
    return(x)
}

append <- function(x, y) {
    return(paste0(x, y))
}

slice <- function(x, y, s) {
    return(substr(s, x, y))
}

index <- function(n, x) {
    return(substr(x, n, n))
}

map <- function(f, x) {
    return(sapply(x, f))
}

identity <- function(x) {
    return(x)
}

cons <- function(x, y) {
    return(c(x, y))
}

car <- function(x) {
    return(x[1])
}

cdr <- function(x) {
    return(x[-1])
}
