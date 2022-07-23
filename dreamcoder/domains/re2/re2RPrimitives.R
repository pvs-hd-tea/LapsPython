library(glue)
library(stringr)

rdot <- "."

rempty <- ""

rvowel <- "(a|e|i|o|u)"

rconsonant <- "[^aeiou]"

a <- "a"

b <- "b"

c <- "c"

d <- "d"

e <- "e"

f <- "f"

g <- "g"

h <- "h"

i <- "i"

j <- "j"

k <- "k"

l <- "l"

m <- "m"

n <- "n"

o <- "o"

p <- "p"

q <- "q"

r <- "r"

s <- "s"

t <- "t"

u <- "u"

v <- "v"

w <- "w"

x <- "x"

y <- "y"

z <- "z"

rnot <- function(s) {
    glue("[^{s}]")
}

ror <- function(s1, s2) {
    glue("(({s1}|{s2}))")
}

rconcat <- function(s1, s2) {
    c(s1, s2)
}

ismatch <- function(s1, s2) {
    str_match(s1, s2) == s1
}

regex_split <- function(s1, s2) {
    if (nchar(s2) == 0)
        s1 <- "."
    ret <- c()
    remaining <- s2
    m <- str_locate(remaining, s1)
    while (!is.na(m[1])) {
        prefix <- substr(remaining, 1, m[1]-1)
        if (nchar(prefix) > 0)
            ret <- c(ret, prefix)
        ret <- c(ret, substr(remaining, m[1], m[2]))
        remaining <- substr(remaining, m[2]+1, nchar(remaining))
        m <- str_locate(remaining, s1)
    }
    if (nchar(remaining) > 0)
        ret <- c(ret, remaining)
    return(ret)
}

rmatch <- function(s1, s2) {
    ismatch(s1, s2)
}

rsplit <- function(s1, s2) {
    regex_split(s1, s2)
}

rflatten <- function(l) {
    paste(l, collapse="")
}

rtail <- function(l) {
    l[length(l)]
}

rappend <- function(x, l) {
    c(x, l)
}

rrevcdr <- function(l) {
    l[-length(l)]
}
