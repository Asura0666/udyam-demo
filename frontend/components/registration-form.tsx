/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import type React from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { DynamicField } from "@/components/DynamicField";
import { UDYAM_FORM_SCHEMA } from "@/lib/form-schema";
import { createFormSchema } from "@/lib/form-validation";
import ProgressTracker from "./ProgressTracker";
import {
  sendAadhaarOtp,
  submitUdyamRegistration,
  verifyAadhaarOtp,
  verifyPan,
} from "@/lib/api";

type FormStep = "aadhaar" | "otp" | "pan" | "success";

export default function RegistrationForm() {
  const [currentStep, setCurrentStep] = useState<FormStep>("aadhaar");
  const [aadhaarVerified, setAadhaarVerified] = useState(false);
  const [panVerified, setPanVerified] = useState(false);
  const [otpSentTo, setOtpSentTo] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [showOtpField, setShowOtpField] = useState(false);
  const [aadhaarData, setAadhaarData] = useState<any>({});
  const [appId, setAppId] = useState("");
  const [transactionId, setTransactionId] = useState("");

  const aadhaarForm = useForm({
    resolver: zodResolver(createFormSchema(UDYAM_FORM_SCHEMA.steps[0])),
    defaultValues: {
      aadhaarNumber: "",
      entrepreneurName: "",
      consent: false,
    },
  });

  const panForm = useForm({
    resolver: zodResolver(createFormSchema(UDYAM_FORM_SCHEMA.steps[1])),
    defaultValues: {
      typeOfOrganisation: "1",
      panNumber: "",
      panHolderName: "",
      dobOrDoi: "",
      panConsent: false,
      previousYearITR: "",
      hasGSTIN: "",
    },
  });

  const otpForm = useForm({
    defaultValues: { otp: "" },
  });

  // ✅ Aadhaar Step
  const handleAadhaarSubmit = async (data: any) => {
    try {
      setErrorMessage("");
      const res = await sendAadhaarOtp({
        aadhaarNumber: data.aadhaarNumber,
        entrepreneurName: data.entrepreneurName,
        consent: data.consent,
      });
      setAadhaarData(data);
      setAppId(res.appId);
      setTransactionId(res.transactionId);
      setOtpSentTo(`******${data.aadhaarNumber.slice(-4)}`);
      setShowOtpField(true);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.message || "Failed to send OTP.");
    }
  };

  // ✅ OTP Step
  const handleOtpSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log(appId, transactionId);

    try {
      setErrorMessage("");
      const res = await verifyAadhaarOtp({
        app_id: appId,
        transaction_id: transactionId,
        otp: otpForm.getValues().otp,
      });
      if (res.verified) {
        setAadhaarVerified(true);
        setSuccessMessage("Your Aadhaar has been successfully verified.");
        setShowOtpField(false);
        setCurrentStep("pan");
      } else {
        setErrorMessage("Invalid OTP. Please try again.");
      }
    } catch (err: any) {
      setErrorMessage(
        err.response?.data?.message || "OTP verification failed."
      );
    }
  };

  // ✅ PAN Step
  const handlePanSubmit = async (data: any) => {
    try {
      setErrorMessage("");
      const res = await verifyPan({
        appId,
        panNumber: data.panNumber,
        panHolderName: data.panHolderName,
        dobOrDoi: data.dobOrDoi,
        consent: data.panConsent,
      });
      if (res.verified) {
        setPanVerified(true);
        setSuccessMessage("Your PAN has been successfully verified.");
      } else {
        setPanVerified(false);
        setErrorMessage("PAN verification failed.");
      }
    } catch (err: any) {
      setErrorMessage(
        err.response?.data?.message || "PAN verification failed."
      );
    }
  };

  // ✅ Final Step
  const handleContinue = async () => {
    try {
      setErrorMessage("");
      const values = panForm.getValues() as {
        typeOfOrganisation: string;
        dobOrDoi: string;
        previousYearITR: string;
        hasGSTIN: string;
      };

      await submitUdyamRegistration(appId, {
        entrepreneurName: aadhaarData.entrepreneurName,
        typeOfOrganisation: values.typeOfOrganisation,
        dobOrDoi: values.dobOrDoi,
        previousYearITR: values.previousYearITR,
        hasGSTIN: values.hasGSTIN,
      });

      setCurrentStep("success");
    } catch (err: any) {
      setErrorMessage(err.response?.data?.message || "Submission failed.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4">
      <div className="flex gap-8">
        <div className="flex-1 max-w-7xl mx-auto px-4">
          <div className="bg-white rounded-sm shadow-sm border border-gray-200">
            <div className="bg-[#007BFF] text-white px-6 py-2 rounded-t-sm">
              <h2 className="text-lg">Aadhaar Verification With OTP</h2>
            </div>

            <div className="p-8">
              {/* Aadhaar Form - Always visible */}
              <form onSubmit={aadhaarForm.handleSubmit(handleAadhaarSubmit)}>
                <div className="grid md:grid-cols-2 gap-8 mb-6">
                  {UDYAM_FORM_SCHEMA.steps[0].fields
                    .filter((field) => field.type !== "checkbox")
                    .map((field) => (
                      <DynamicField
                        key={field.name}
                        field={field}
                        register={aadhaarForm.register}
                        errors={aadhaarForm.formState.errors}
                        watch={aadhaarForm.watch}
                        disabled={aadhaarVerified}
                      />
                    ))}
                </div>

                {/* Instructions */}
                <div className="mb-8">
                  <ul className="space-y-4 text-sm text-gray-800 leading-relaxed">
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>
                        Aadhaar number shall be required for Udyam Registration.
                      </span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>
                        The Aadhaar number shall be of the proprietor in the
                        case of a proprietorship firm, of the managing partner
                        in the case of a partnership firm and of a karta in the
                        case of a Hindu Undivided Family (HUF).
                      </span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2">•</span>
                      <span>
                        In case of a Company or a Limited Liability Partnership
                        or a Cooperative Society or a Society or a Trust, the
                        organisation or its authorised signatory shall provide
                        its GSTIN(As per applicability of CGST Act 2017 and as
                        notified by the ministry of MSME{" "}
                        <a
                          href="docs/225669.pdf"
                          target="_blank"
                          className="text-blue-600 underline hover:text-blue-800"
                          rel="noreferrer"
                        >
                          vide S.O. 1055(E) dated 05th March 2021
                        </a>
                        ) and PAN along with its Aadhaar number.
                      </span>
                    </li>
                  </ul>
                </div>

                {/* Checkbox Fields */}
                {UDYAM_FORM_SCHEMA.steps[0].fields
                  .filter((field) => field.type === "checkbox")
                  .map((field) => (
                    <div key={field.name} className="mb-8">
                      <DynamicField
                        field={field}
                        register={aadhaarForm.register}
                        errors={aadhaarForm.formState.errors}
                        watch={aadhaarForm.watch}
                        disabled={aadhaarVerified}
                      />
                    </div>
                  ))}

                {/* Submit Button */}
                {!aadhaarVerified && !showOtpField && (
                  <div className="form-group">
                    <Button
                      type="submit"
                      className="bg-[#007BFF] hover:bg-[#0056B3] text-white px-8 py-3 rounded-md font-medium text-base"
                      disabled={aadhaarForm.formState.isSubmitting}
                    >
                      Validate &amp; Generate OTP
                    </Button>
                  </div>
                )}
              </form>

              {/* OTP Field */}
              {showOtpField && (
                <div className="mb-8 p-4 bg-blue-50 border border-blue-200 rounded-md">
                  <form onSubmit={handleOtpSubmit}>
                    <label className="block text-black font-medium mb-3">
                      <span className="text-red-500">*</span> Enter One Time
                      Password(OTP) Code
                    </label>
                    <input
                      {...otpForm.register("otp")}
                      type="text"
                      maxLength={6}
                      placeholder="OTP code"
                      className="w-full h-12 px-4 border border-gray-300 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500 mb-2"
                    />
                    <p className="text-sm text-gray-600 mb-4">
                      OTP has been sent to {otpSentTo}
                    </p>
                    <Button
                      type="submit"
                      className="bg-[#007BFF] hover:bg-[#0056B3] text-white px-8 py-3 rounded-md font-medium text-base"
                    >
                      Validate
                    </Button>
                  </form>
                </div>
              )}

              {/* Success Message for Aadhaar */}
              {aadhaarVerified && (
                <Alert className="mb-6 border-green-200 bg-green-50">
                  <AlertDescription className="text-green-800 font-medium">
                    {successMessage}
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </div>

          {/* PAN Section - Show after Aadhaar verification */}
          {(currentStep === "pan" || panVerified) && (
            <div className="bg-white rounded-sm shadow-sm border border-gray-200 mt-6">
              <div className="bg-green-600 text-white px-6 py-2 rounded-t-sm">
                <h2 className="text-lg">PAN Verification</h2>
              </div>

              <div className="p-8">
                {/* PAN Form */}
                <form onSubmit={panForm.handleSubmit(handlePanSubmit)}>
                  {Object.keys(panForm.formState.errors).length > 0 && (
                    <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                      <p className="text-red-800 font-medium">
                        Form Validation Errors:
                      </p>
                      <ul className="text-sm text-red-700 mt-2">
                        {Object.entries(panForm.formState.errors).map(
                          ([key, error]) => (
                            <li key={key}>
                              • {key}: {error?.message}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}

                  <div className="grid md:grid-cols-2 gap-8 mb-6">
                    {UDYAM_FORM_SCHEMA.steps[1].fields
                      .filter(
                        (field) =>
                          field.type !== "checkbox" && field.type !== "radio"
                      )
                      .map((field) => (
                        <DynamicField
                          key={field.name}
                          field={field}
                          register={panForm.register}
                          errors={panForm.formState.errors}
                          watch={panForm.watch}
                          disabled={
                            panVerified && field.name !== "typeOfOrganisation"
                          }
                        />
                      ))}
                  </div>

                  {/* Checkbox Fields */}
                  {UDYAM_FORM_SCHEMA.steps[1].fields
                    .filter((field) => field.type === "checkbox")
                    .map((field) => (
                      <div key={field.name} className="mb-8">
                        <DynamicField
                          field={field}
                          register={panForm.register}
                          errors={panForm.formState.errors}
                          watch={panForm.watch}
                          disabled={panVerified}
                        />
                      </div>
                    ))}

                  {/* Submit Button */}
                  {!panVerified && (
                    <div className="form-group">
                      <Button
                        type="submit"
                        className="bg-[#007BFF] hover:bg-[#0056B3] text-white px-8 py-3 rounded-md font-medium text-base"
                        disabled={panForm.formState.isSubmitting}
                        onClick={() => {
                          console.log("PAN Validate button clicked");
                          console.log("Form values:", panForm.getValues());
                          console.log("Form errors:", panForm.formState.errors);
                          console.log(
                            "Form is valid:",
                            panForm.formState.isValid
                          );
                        }}
                      >
                        PAN Validate
                      </Button>
                    </div>
                  )}
                </form>

                {panVerified && (
                  <div className="mt-8 space-y-6">
                    {UDYAM_FORM_SCHEMA.steps[1].fields
                      .filter(
                        (field) => field.type === "radio" && field.conditional
                      )
                      .map((field) => (
                        <DynamicField
                          key={field.name}
                          field={field}
                          register={panForm.register}
                          errors={panForm.formState.errors}
                          watch={panForm.watch}
                          disabled={false}
                        />
                      ))}
                  </div>
                )}

                {/* Continue Button */}
                {panVerified && currentStep !== "success" && (
                  <div className="form-group mt-6">
                    <Button
                      onClick={handleContinue}
                      className="bg-[#007BFF] hover:bg-[#0056B3] text-white px-8 py-3 rounded-md font-medium text-base"
                    >
                      Continue
                    </Button>
                  </div>
                )}

                {/* Success Message for PAN */}
                {panVerified && (
                  <Alert className="mb-6 border-green-200 bg-green-50">
                    <AlertDescription className="text-green-800 font-medium">
                      {successMessage}
                    </AlertDescription>
                  </Alert>
                )}

                {/* Error Messages */}
                {errorMessage && (
                  <Alert className="mb-6 border-red-200 bg-red-50">
                    <AlertDescription className="text-red-800 font-medium">
                      {errorMessage}
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </div>
          )}

          {/* Success Step */}
          {currentStep === "success" && (
            <div className="bg-white rounded-sm shadow-sm border border-gray-200 mt-6">
              <div className="p-8 text-center">
                <h2 className="text-2xl font-bold text-green-600 mb-4">
                  Registration Successful!
                </h2>
                <p className="text-gray-700">
                  Your Udyam Registration form has been submitted successfully.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Progress Tracker - Right Side */}
        <div className="hidden lg:block w-80">
          <ProgressTracker
            currentStep={currentStep}
            aadhaarVerified={aadhaarVerified}
            panVerified={panVerified}
          />
        </div>
      </div>
    </div>
  );
}
