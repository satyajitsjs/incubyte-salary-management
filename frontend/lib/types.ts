export type Employee = { id:string; employee_id:string; first_name:string; last_name:string; full_name:string; email:string; department:string; job_title:string; job_level:string; country:string; currency:string; annual_salary:string; exchange_rate_to_usd:string; annual_salary_usd:string; hire_date:string; created_at:string; updated_at:string };
export type Page<T> = {count:number; next:string|null; previous:string|null; results:T[]};
export type Summary = {employee_count:number; total_payroll_usd:string; average_salary_usd:string; median_salary_usd:string; min_salary_usd:string; max_salary_usd:string};
export type GroupRow = {department?:string; country?:string; employee_count:number; total_payroll_usd:string; average_salary_usd:string};
export type DistributionRow = {label:string; min:number; max:number|null; employee_count:number};
export type Metadata = {departments:string[]; countries:string[]; job_levels:{value:string;label:string}[]};
export type SalaryChange = {id:string;previous_salary:string;new_salary:string;previous_currency:string;new_currency:string;exchange_rate_to_usd:string;previous_salary_usd:string;new_salary_usd:string;effective_date:string;reason:string;created_at:string};
