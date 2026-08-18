import type { LucideIcon } from "lucide-react";
export function StatCard({label,value,caption,icon:Icon}:{label:string;value:string;caption:string;icon:LucideIcon}){return <div className="card statCard"><div className="statTop"><span>{label}</span><div className="iconChip"><Icon size={18}/></div></div><strong>{value}</strong><small>{caption}</small></div>}
