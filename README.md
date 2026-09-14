<!--toc:start-->

- [DimAlysis](#dimalysis)
- [Installing](#installing)
- [Help](#help)
- [Example](#example)
  - [Defining a few things](#defining-a-few-things)
    - [1. Our Solution variable and its dimension](#1-our-solution-variable-and-its-dimension)
    - [2. The parameters our solution variable depends on and their dimensions](#2-the-parameters-our-solution-variable-depends-on-and-their-dimensions)
  - [Constructing our dimensional matrix](#constructing-our-dimensional-matrix)
  - [Running DimAlysis](#running-dimalysis)
  - [Analyzing the output](#analyzing-the-output)

<!--toc:end-->

# DimAlysis

Tool for computing Pi-groups for dimensional analysis via exponent algebra

# Installing

_Note: Must have `uv` installed on system_

To install this tool: run the following command:

`uv tool install git+https://github.com/BenRider45/DimAlysis`

# Help

To see help message, run `dimalysis --help`

# Example

Lets derive the formula for the period of a simple pendulum using DimAlysis!

> [!NOTE] Note on dimension
> Dimensional analysis uses the concept of SI dimensions Mass ($M$), Length ($L$), Time ($T$), and sometimes Temperature ($\Theta$). These quantities are also known as Extensive properties! The parameters used in dimensional analysis should be able to be expressed in terms of Extensive properties.

## Defining a few things

### 1. Our Solution variable and its dimension

In this case, our solution variable is $P$, the period of the pendulum, and has dimension [$T$]

### 2. The parameters our solution variable depends on and their dimensions

In this case $P$ depends on

- Length of the pendulum arm $l$ (has dimension [$L$])
- Weight of the mass on the end of the pendulum arm (has dimension [$MLT^-2$])
- Force of gravity $g$ (has dimension [$LT^-2$])

## Constructing our dimensional matrix

Now that we have defined these things, we can construct the dimensional matrix
for DimAlysis, this matrix should be input in column major order (dimension order $M,L,T$), with spaces separating each number:

Our dimensional matrix becomes:

```
    P  l  w  g
M [ 0  0  1  0]
L [ 0  1  1  1]
T [ 1  0 -2 -2]
```

## Running DimAlysis

Now, we input this matrix into DimAlysis in the proper format, and also specify out solution variable with the following command:

`dimalysis "P,l,w,g" "0 0 1 0 1 0 1 1 -2 0 1 -2" P`

This command should provide the output:

```
Dimensional Matrix: (Rows in order M L T)
[[ 0  0  1  0]
 [ 0  1  1  1]
 [ 1  0 -2 -2]]
SolnbVarCol: 0
Choose from the following sets of variables to be the repeating parameters:
0: l,w,g
```

_Note: The way this problem works out, we only have one choice of repeating parameters, usually there will be more options_

After entering 0 to choose our repeating parameters, we get the output

```
{'Group 0:': (' P * l^-0.5*w^-0.0*g^0.5',)}
```

## Analyzing the output

The output of Dimalysis gives us each dimensional group as a function of one of our non-repeating parameters with exponent $1$, and out repeaeting parameters, each with an exponent

In this case our only non-dimensional group (AKA, $\Pi$ group) is $\Pi_0 = Pl^{-0.5}w^0g^{0.5}$

We know that this is the expected number of $\Pi$-groups from the Buckingham $\Pi$ Theorem, which says that for a $n$-variable problem which spans over $r$ dimensions, we can formulate an equation relating all of the variables with $(n-r)$ non-dimensional $\Pi$ groups. Our output is consistent with this since $4-3 =1$.

With this information, we can draw the conclusion that $P = \Psi( \sqrt{\frac{l}{g}})$ where $\Psi$ is some function.
This corresponds with reality (check any physics textbook to compare the result!)
