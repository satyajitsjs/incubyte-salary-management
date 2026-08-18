export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, cache: "no-store" });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try { const body = await response.json(); message = body.detail ?? JSON.stringify(body); } catch {}
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const moneyUSD = (value: string | number) => new Intl.NumberFormat("en-US", {style:"currency", currency:"USD", maximumFractionDigits:0}).format(Number(value));
export const moneyLocal = (value: string | number, currency: string) => new Intl.NumberFormat(undefined, {style:"currency", currency, maximumFractionDigits:0}).format(Number(value));
export const compact = (value: string | number) => new Intl.NumberFormat("en-US", {notation:"compact", maximumFractionDigits:1}).format(Number(value));
