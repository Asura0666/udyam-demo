// src/lib/api.ts
import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE as string;

// Helper to format DD/MM/YYYY → YYYY-MM-DD
function formatDate(dateStr: string) {
  if (!dateStr) return "";
  const parts = dateStr.split("/");
  if (parts.length === 3) {
    const [day, month, year] = parts;
    return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
  }
  return dateStr;
}

// Aadhaar: Send OTP
export async function sendAadhaarOtp(data: {
  aadhaarNumber: string;
  entrepreneurName: string;
  consent: boolean;
}) {
  const res = await axios.post(`${API_BASE}/aadhaar/send-otp`, data);
  return res.data;
}

// Aadhaar: Verify OTP
export async function verifyAadhaarOtp(data: {
  app_id: string;
  transaction_id: string;
  otp: string;
}) {
  const res = await axios.post(`${API_BASE}/aadhaar/verify-otp`, data);
  return res.data;
}

// PAN: Verify
export async function verifyPan(data: {
  appId: string;
  panNumber: string;
  panHolderName: string;
  dobOrDoi: string;
  consent: boolean;
}) {
  const payload = {
    ...data,
    dobOrDoi: formatDate(data.dobOrDoi),
  };
  const res = await axios.post(`${API_BASE}/pan/verify`, payload);
  return res.data;
}

// Udyam: Submit registration
export async function submitUdyamRegistration(
  appId: string,
  data: {
    entrepreneurName: string;
    typeOfOrganisation: string;
    dobOrDoi: string;
    previousYearITR: string;
    hasGSTIN: string;
  }
) {
  const payload = {
    ...data,
    dobOrDoi: formatDate(data.dobOrDoi),
  };
  const res = await axios.post(
    `${API_BASE}/udyam/${appId}/submit`,
    payload
  );
  return res.data;
}
