import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
export const metadata:Metadata={title:"ACME Compensation Manager",description:"HR salary management and compensation analytics"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><div className="appShell"><Sidebar/><main className="main">{children}</main></div></body></html>}
