#KJN Stuff
#Constant pointing to the database. DO NOT CHANGE.
#KJN -- DISCUSS WITH OTHERS GOING FORWARD
from ..database import CourseDAO
from ..database import StudentDAO
from ..database import UserDAO
from ..database import SemesterDAO
from ..database import QuestionDAO
from ..database import FacultyDAO
from ..database import ConcentrationDAO
from ..database import RecommendationDAO
from .. import db

#Constants used for database purposes
studentDao  = StudentDAO.StudentDAO(db)
facultyDao  = FacultyDAO.FacultyDAO(db)
courseDao   = CourseDAO.CourseDAO(db)
userDao     = UserDAO.UserDAO(db)
semesterDao = SemesterDAO.SemesterDAO(db)
questionDao = QuestionDAO.QuestionDAO(db)
concentrationDao = ConcentrationDAO.ConcentrationDAO(db)
recommendationDao = RecommendationDAO.RecommendationDAO(db)

semesterToUse = 1 ### FOR NOW, HARD CODE OUR SEMESTER I


