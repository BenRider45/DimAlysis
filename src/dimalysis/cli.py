import numpy as np
import typer
import pprint
from dimalysis import utils
from typing import Annotated

app = typer.Typer()


@app.command()
def getPiGroups(
    paramNames: Annotated[
        str, typer.Argument(help="list of the parameters in analysis (comma separated)")
    ],
    dimMatrix: Annotated[
        str,
        typer.Argument(
            help="Dimensional matrix for all parameters in same order as paramNames plugin "
        ),
    ],
    solutionVariable: Annotated[
        str,
        typer.Argument(
            help="The variable in which we are doing the dimensional analysis for"
        ),
    ],
    numberOfDimensions: Annotated[
        int, typer.Argument(help="Number of Dimensions used ")
    ] = 3,
    repeatingParams: Annotated[
        str,
        typer.Argument(
            help="indicies (comma separated) of the columns of paramNames which you would like to use as your set of repeatingParams"
        ),
    ] = "-1",
):

    paramNamesArr = np.array(paramNames.split(","))
    dimMat = (
        np.fromstring(dimMatrix, dtype=int, sep=" ")
        .reshape(paramNamesArr.size, numberOfDimensions)
        .transpose()
    )
    # order ot dims is M L T
    print("Dimensional Matrix: (Rows in order M L T) ")
    print(dimMat)
    if solutionVariable not in paramNamesArr:
        print(
            f"ERROR: Solution Variable {solutionVariable} is not included in parameter list \n"
        )
        return

    solnVarCol = paramNames.index(solutionVariable)
    print(f"SolnbVarCol: {solnVarCol}")
    if dimMat.shape[1] != paramNamesArr.size:
        print("ERROR: Must include Dimensions for all parameters")
    r = np.linalg.matrix_rank(dimMat)

    if repeatingParams == "-1":
        print("In default Path")
        possibleRepParams = utils.rSubset(
            [x for x in range(paramNamesArr.size) if x != solnVarCol], r
        )
        validRepParams = list(
            filter(lambda x: np.linalg.det(dimMat[:, x]) != 0, possibleRepParams)
        )
        print(validRepParams)
        print(
            "Choose from the following sets of variables to be the repeating parameters:"
        )
        for i in range(len(validRepParams)):
            print(f"{i}: {','.join(paramNamesArr[x] for x in validRepParams[i])}")
        RepParamsChoice = int(input("Choice: "))

        repeatingParams = np.array(validRepParams[RepParamsChoice])
        print(f"repeatingParams: {paramNamesArr[repeatingParams]}")
    else:
        repeatingParams = np.fromstring(repeatingParams, dtype=int, sep=" ")
        print(f"repeatingParams: {repeatingParams}")
        if len(repeatingParams) != r:
            # TODO what if we allowed someone to name two of the repeatingParams and then provided the results for the remaining options!
            print("ERROR: Not Enough Dimensional Variables Set")
            return
        if np.linalg.det(dimMat[:, repeatingParams]) == 0:
            print(f"Det: {np.linalg.det(dimMat[:, repeatingParams])} ")
            print(
                "ERROR: Selected set of repeating parameters is does not fufill the requirement (Determinant is zero!!!)"
            )
            return

    print(
        f"Det: {np.linalg.det(dimMat[:, repeatingParams])}\n Rank: {np.linalg.matrix_rank(dimMat[:, repeatingParams])}"
    )
    repeatingParamsDimMat = dimMat[:, repeatingParams]
    print(f"repeatingParamsIdx: {repeatingParams}")
    varsToAdd = [x for x in range(paramNamesArr.size) if x not in repeatingParams]
    output_dict = {}
    i = 0
    for n in varsToAdd:
        b = dimMat[:, n] * -1
        x = np.linalg.solve(repeatingParamsDimMat, b)
        output_dict[f"Group {i}:"] = (
            f" {paramNamesArr[n]} * {'*'.join(f'{paramNamesArr[repeatingParams[n]]}^{x[n]}' for n in range(x.size))}",
        )
        i = i + 1

    pprint.pprint(output_dict)


if __name__ == "__main__":
    app()
