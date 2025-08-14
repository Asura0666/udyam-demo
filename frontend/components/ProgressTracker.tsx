import { CheckCircle, Circle } from "lucide-react"

interface ProgressTrackerProps {
  currentStep: "aadhaar" | "otp" | "pan" | "success"
  aadhaarVerified: boolean
  panVerified: boolean
}

export default function ProgressTracker({ currentStep, aadhaarVerified, panVerified }: ProgressTrackerProps) {
  const steps = [
    {
      id: "aadhaar",
      title: "Step 1",
      subtitle: "Aadhaar Verification",
      completed: aadhaarVerified,
      active: currentStep === "aadhaar" || currentStep === "otp",
    },
    {
      id: "pan",
      title: "Step 2",
      subtitle: "PAN Verification",
      completed: panVerified,
      active: currentStep === "pan" || currentStep === "success",
    },
  ]

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-6 sticky top-24">
      <h3 className="text-lg font-semibold text-gray-800 mb-6">Registration Progress</h3>

      <div className="space-y-6">
        {steps.map((step, index) => (
          <div key={step.id} className="relative">
            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className={`absolute left-4 top-8 w-0.5 h-12 ${step.completed ? "bg-green-500" : "bg-gray-300"}`} />
            )}

            {/* Step Content */}
            <div className="flex items-start space-x-3">
              {/* Step Icon */}
              <div className="flex-shrink-0">
                {step.completed ? (
                  <CheckCircle className="w-8 h-8 text-green-500" />
                ) : (
                  <Circle className={`w-8 h-8 ${step.active ? "text-blue-500" : "text-gray-400"}`} />
                )}
              </div>

              {/* Step Text */}
              <div className="flex-1 min-w-0">
                <p
                  className={`text-sm font-medium ${
                    step.completed ? "text-green-600" : step.active ? "text-blue-600" : "text-gray-500"
                  }`}
                >
                  {step.title}
                </p>
                <p
                  className={`text-xs ${
                    step.completed ? "text-green-500" : step.active ? "text-blue-500" : "text-gray-400"
                  }`}
                >
                  {step.subtitle}
                </p>

                {/* Status Badge */}
                <div className="mt-1">
                  {step.completed ? (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Completed
                    </span>
                  ) : step.active ? (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      In Progress
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                      Pending
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Progress Bar */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex justify-between text-xs text-gray-600 mb-2">
          <span>Progress</span>
          <span>{aadhaarVerified && panVerified ? "100%" : aadhaarVerified ? "50%" : "0%"}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
            style={{
              width: aadhaarVerified && panVerified ? "100%" : aadhaarVerified ? "50%" : "0%",
            }}
          />
        </div>
      </div>
    </div>
  )
}
