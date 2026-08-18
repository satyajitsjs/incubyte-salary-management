"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, FileUp, LayoutDashboard, Users, WalletCards } from "lucide-react";
const items=[{href:"/",label:"Dashboard",icon:LayoutDashboard},{href:"/employees",label:"Employees",icon:Users},{href:"/import",label:"Import CSV",icon:FileUp}];
export function Sidebar(){ const path=usePathname(); return <aside className="sidebar"><div className="brand"><div className="brandMark"><WalletCards size={20}/></div><div><strong>ACME</strong><span>Compensation</span></div></div><nav>{items.map(({href,label,icon:Icon})=>{const active=href==="/"?path===href:path.startsWith(href);return <Link key={href} href={href} className={active?"navItem active":"navItem"}><Icon size={18}/>{label}</Link>})}</nav><div className="sidebarNote"><BarChart3 size={18}/><div><strong>Synthetic demo</strong><span>Reporting currency: USD</span></div></div></aside> }
