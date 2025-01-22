"""
This code is the intellectual property of IBM and is not to be used by non-IBM practitioners 
nor distributed outside of IBM internal without having the proper clearance. 
For full usage guidelines refer to Guidelines for Code Accelerator Consumption. 
https://w3.ibm.com/services/lighthouse/help-and-support/terms#asset-consumption

@author Benjamin A. Janes (benjamin.janes@se.ibm.com)
"""

from pydantic.fields import Field
from pydantic.main import BaseModel


class ExceptionResponse(BaseModel):
    filename: str = Field(..., description="Name of the file with the exception")
    message: str = Field(..., description="The error message")
    exceptionClass: str = Field(..., description="Class of the exception")
    lineno: int = Field(..., description="Line number with error")
    codeLine: str = Field(..., description="Line of code with exception in")
    errStr: str = Field(..., description="Formated exception string for log")


class GenericResponse(BaseModel):
    result: str = Field(..., description="The output string")

    class Config:
        from_attributes = True


class StatusResponse(BaseModel):
    status: str = Field(..., description="Status string")

    class Config:
        from_attributes = True


class CVAnalysisResponse(BaseModel):
    betyg: int = Field(..., description="The rating of the CV")
    orsak: str = Field(..., description="Why the rating was given to the CV")
    behövs_mer: bool = Field(..., description="Is more information needed to complete the rating")
    försäkringskassan: bool = Field(..., description="Has the applicant worked at Försäkringskassan")

    class Config:
        from_attributes = True
