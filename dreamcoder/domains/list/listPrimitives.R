flatten <- function(l) {
    return(unlist(l))
}

range <- function(n) {
    return(1:n)
}

if <- function(c, t, f) {
    if(c)
        return(t)
    else
        return(f)
}

and <- function(x, y) {
    return(x && y)
}


or <- function(x, y) {
    return(x || y)
}

addition <- function(x){
    return(x + y)
}

subtraction<- function(x, y) {
    return(x - y)
}

multiplication <- function(x, y) {
    return(x * y)
}

negate <- function(x) {
    return(-x)
}

reverse <- function(x) {
    return(rev(x))
}

append <- function(x, y) {
    return(append(x, y))
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

isEmpty <- function(x) {
    return(length(x) == 0)
}

single <- function(x) {
    return(c(x))
}

slice(x, y, l) {
    return(l[x:y])
}


map <- function(f, l) {
    return(sapply(l, f))
}

zip <- function(a, b, f) {
    return(f(a, b))
}


mapi <- function(f, l) {
    return(f(1:length(l), l))
}

reduce <- function(f, x0, l) {
    for (a in l)
        x0 <- f(a, x0)
    return(x0)
}

reducei <- function(f, x0, l) {
    for (i in 1:length(l))
        x0 <- f(i, a[i], x0)
    return(x0)
}

fold <- function (l, x0, f) {
    for (a in rev(l))
        x0 <- f(a, x0)
    return(x0)
}

eq <- function(x, y) {
    return(x == y)
}

eq0 <- function(x) {
    return(x == 0)
}

a1 <- function(x) {
    return(x + 1)
}

d1 <- function(x) {
    return(x - 1)
}

mod <- function(x, y) {
    return(x %% y)
}

not <- function(x) {
    return(!x)
}

gt <- function(x, y) {
    return(x > y)
}

gt <- function(x, y) {
    return(x < y)
}

index(j, l) {
    return(l[j])
}


replace <- function(f, lnew, lin) {
    for(i in 1:length(lin))
        if(f(i, lin[i]))
            lin[i] <- lnew
    return(unlist(lin))
}


isPrime <- function(n) {
    return(n %in% c(
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199))
}

isSquare <- function(n) {
    return(as.integer(sqrt(n))^2 == n)
}

appendmap(f, xs) {
    return(f(xs))
}

filter(f, l) {
    return(Filter(f, l))
}

any <- function(f, l) {
    return(any(f(l)))
}

all <- function(f, l) {
    return(all(f(l)))
}

find <- function(x, l) {
    return(x %in% l)
}

unfold <- function(x, p, h, n) {
    return(unfold_recursive(p, f, n, x))
}

unfold_recursive <- function(p, f, n, x, recursion_limit=50) {
    if(recursion_limit <= 0)
        stop()
    if(p(x))
        return(c())
    return(c(f(x), unfold_recursive(p, f, n, n(x), recursion_limit - 1)))
}

curry(f, x, y) {
    return(f(x, y))
}

match <- function(l, b, f) {
    if(length(l) == 0)
        return(b)
    return(f(l[1], l[-1]))
}