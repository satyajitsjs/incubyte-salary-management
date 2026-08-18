"use client";
import { useEffect, useState } from "react";
import { Banknote, CircleDollarSign, Gauge, UsersRound } from "lucide-react";
import { apiFetch, compact, moneyUSD } from "@/lib/api";
import type { DistributionRow, GroupRow, Summary } from "@/lib/types";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { BarList } from "@/components/BarList";

export default function Dashboard(){
 const [summary,setSummary]=useState<Summary|null>(null),[dept,setDept]=useState<GroupRow[]>([]),[country,setCountry]=useState<GroupRow[]>([]),[dist,setDist]=useState<DistributionRow[]>([]),[error,setError]=useState("");
 useEffect(()=>{Promise.all([apiFetch<Summary>("/analytics/summary/"),apiFetch<GroupRow[]>("/analytics/by_department/"),apiFetch<GroupRow[]>("/analytics/by_country/"),apiFetch<DistributionRow[]>("/analytics/salary_distribution/")]).then(([s,d,c,x])=>{setSummary(s);setDept(d);setCountry(c);setDist(x)}).catch(e=>setError(e.message))},[]);
 if(error)return <section><PageHeader eyebrow="Overview" title="Compensation dashboard" description="Organization-wide salary reporting."/><div className="errorBox">Could not load the API: {error}</div></section>;
 if(!summary)return <div className="loading">Loading compensation analytics…</div>;
 const maxDist=Math.max(...dist.map(x=>x.employee_count),1);
 return <section><PageHeader eyebrow="Overview" title="Compensation dashboard" description="A normalized view of how ACME pays 10,000 people across countries and teams."/>
 <div className="statsGrid"><StatCard label="Employees" value={compact(summary.employee_count)} caption="Active compensation records" icon={UsersRound}/><StatCard label="Annual payroll" value={moneyUSD(summary.total_payroll_usd)} caption="Normalized reporting value" icon={Banknote}/><StatCard label="Average salary" value={moneyUSD(summary.average_salary_usd)} caption="Normalized USD" icon={CircleDollarSign}/><StatCard label="Median salary" value={moneyUSD(summary.median_salary_usd)} caption="Less sensitive to outliers" icon={Gauge}/></div>
 <div className="twoCol"><div className="card panel"><div className="panelTitle"><div><span>Payroll by department</span><small>Top departments by normalized annual payroll</small></div></div><BarList rows={dept} keyName="department"/></div><div className="card panel"><div className="panelTitle"><div><span>Payroll by country</span><small>Cross-country comparison using stored FX snapshots</small></div></div><BarList rows={country} keyName="country"/></div></div>
 <div className="card panel"><div className="panelTitle"><div><span>Salary distribution</span><small>Employee count by normalized annual salary band</small></div><span className="pill">USD reporting</span></div><div className="histogram">{dist.map(x=><div className="histItem" key={x.label}><div className="histValue">{x.employee_count}</div><div className="histBar"><span style={{height:`${Math.max(6,x.employee_count/maxDist*100)}%`}}/></div><div className="histLabel">{x.label}</div></div>)}</div></div>
 </section>}
