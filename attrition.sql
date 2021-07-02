Select gender JobLevel, JobRole, MaritalStatus, MonthlyIncome, 
NumCompaniesWorked, TotalWorkingYears, YearsAtCompany, YearsSinceLastPromotion, 
YearsWithCurrManager
from ST_d2_general_data
where attrition = 'Yes'

Select gender ,JobLevel, JobRole, MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) as Income, 
 YearsSinceLastPromotion, 
YearsWithCurrManager, count(1) as att
from ST_d2_general_data
where attrition = 'Yes'
group by gender, JobLevel, JobRole, MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) , 
 YearsSinceLastPromotion, YearsWithCurrManager
 having count(1)>3
order by count(1) DESC

Select gender , MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) as Income, 
 YearsSinceLastPromotion, 
YearsWithCurrManager, count(1) as att
from ST_d2_general_data
where attrition = 'Yes'
group by gender,  MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) , 
 YearsSinceLastPromotion, YearsWithCurrManager
 having count(1)>3
order by count(1) DESC
NumCompaniesWorked, TotalWorkingYears, YearsAtCompany,


Select  MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) as Income, 
 YearsSinceLastPromotion, 
YearsWithCurrManager, count(1) as att
from ST_d2_general_data
where attrition = 'Yes'
group by MaritalStatus, 
iif(MonthlyIncome<30000,'Low',iif(MonthlyIncome > 30000 and MonthlyIncome<80000,'Medium','High')) , 
 YearsSinceLastPromotion, YearsWithCurrManager
 having count(1)>3
order by count(1) DESC


NumCompaniesWorked, TotalWorkingYears, YearsAtCompany,




select *, yes/no as porc
FROM(
Select gender, cast(sum(iif(attrition='Yes',1,0)) as real) as yes, 
cast(sum(iif(attrition='No',1,0)) as real) as no
from ST_d2_general_data 
group by gender
) aux

select *, yes/no as porc
FROM(
Select MaritalStatus, cast(sum(iif(attrition='Yes',1,0)) as real) as yes, 
cast(sum(iif(attrition='No',1,0)) as real) as no
from ST_d2_general_data 
group by MaritalStatus
) aux

TotalWorkingYears >20 or menor a 1

select *, yes/no as porc
FROM(
Select cast(TotalWorkingYears as INTEGER) TotWorkYears, cast(sum(iif(attrition='Yes',1,0)) as real) as yes, 
cast(sum(iif(attrition='No',1,0)) as real) as no
from ST_d2_general_data 
group by TotalWorkingYears
) aux
order by 1
