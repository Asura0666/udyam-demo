import type { IFormSchema } from "@/types/form"

export const UDYAM_FORM_SCHEMA: IFormSchema = {
  steps: [
    {
      step: 1,
      name: "Aadhaar & OTP Verification",
      fields: [
        {
          name: "aadhaarNumber",
          label: "1. Aadhaar Number / आधार संख्या",
          type: "text",
          placeholder: "Your Aadhaar No",
          validation: {
            required: true,
            maxlength: 12,
            pattern: "^\\d{12}$",
          },
        },
        {
          name: "entrepreneurName",
          label: "2. Name of Entrepreneur / उद्यमी का नाम",
          type: "text",
          placeholder: "Name as per Aadhaar",
          validation: {
            required: true,
            maxlength: 100,
          },
        },
        {
          name: "consent",
          label:
            "I, the holder of the above Aadhaar, hereby give my consent to Ministry of MSME, Government of India, for using my Aadhaar number as alloted by UIDAI for Udyam Registration. NIC / Ministry of MSME, Government of India, have informed me that my aadhaar data will not be stored/shared. / मैं, आधार धारक, इस प्रकार उद्यम पंजीकरण के लिए यूआईडीएआई के साथ अपने आधार संख्या का उपयोग करने के लिए सू0ल0म0उ0 मंत्रालय, भारत सरकार को अपनी सहमति देता हूं। एनआईसी / सू0ल0म0उ0 मंत्रालय, भारत सरकार ने मुझे सूचित किया है कि मेरा आधार डेटा संग्रहीत / साझा नहीं किया जाएगा।",
          type: "checkbox",
          placeholder: null,
          validation: {
            required: true,
            checked: true,
          },
        },
      ],
    },
    {
      step: 2,
      name: "PAN Verification",
      fields: [
        {
          name: "typeOfOrganisation",
          label: "3. Type of Organisation / संगठन के प्रकार",
          type: "select",
          placeholder: null,
          validation: {
            required: true,
          },
          options: [
            {
              text: "1. Proprietary / एकल स्वामित्व",
              value: "1",
            },
            {
              text: "2. Hindu Undivided Family / हिंदू अविभाजित परिवार (एचयूएफ)",
              value: "2",
            },
            {
              text: "3. Partnership / पार्टनरशिप",
              value: "3",
            },
            {
              text: "4. Co-Operative / सहकारी",
              value: "4",
            },
            {
              text: "5. Private Limited Company / प्राइवेट लिमिटेड कंपनी",
              value: "5",
            },
            {
              text: "6. Public Limited Company / पब्लिक लिमिटेड कंपनी",
              value: "6",
            },
            {
              text: "7. Self Help Group / स्वयं सहायता समूह",
              value: "7",
            },
            {
              text: "8. Limited Liability Partnership / सीमित दायित्व भागीदारी",
              value: "9",
            },
            {
              text: "9. Society / सोसाईटी",
              value: "10",
            },
            {
              text: "10. Trust / ट्रस्ट",
              value: "11",
            },
            {
              text: "11. Others / अन्य",
              value: "8",
            },
          ],
        },
        {
          name: "panNumber",
          label: "4.1 PAN / पैन",
          type: "text",
          placeholder: "Enter Pan Number",
          validation: {
            required: true,
            maxlength: 10,
            pattern: "^[A-Z]{5}[0-9]{4}[A-Z]{1}$",
          },
        },
        {
          name: "panHolderName",
          label: "4.1.1 Name of PAN Holder / पैन धारक का नाम",
          type: "text",
          placeholder: "Name as per PAN",
          validation: {
            required: true,
            maxlength: 100,
          },
        },
        {
          name: "dobOrDoi",
          label: "4.1.2 DOB or DOI as per PAN / पैन के अनुसार जन्म तिथि या निगमन तिथि",
          type: "text",
          placeholder: "DD/MM/YYYY",
          validation: {
            required: true,
            pattern: "^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\\d{4}$",
          },
        },
        {
          name: "panConsent",
          label:
            "I, the holder of the above PAN, hereby give my consent to Ministry of MSME, Government of India, for using my data/ information available in the Income Tax Returns filed by me, and also the same available in the GST Returns and also from other Government organizations, for MSME classification and other official purposes, in pursuance of the MSMED Act, 2006.",
          type: "checkbox",
          placeholder: null,
          validation: {
            required: false,
            checked: true,
          },
        },
        {
          name: "previousYearITR",
          label: "Have you filed the ITR for Previous Year(PY) (2023-24) ITR ?",
          type: "radio",
          placeholder: null,
          validation: {
            required: false,
          },
          conditional: true,
          options: [
            {
              text: "Yes",
              value: "1",
            },
            {
              text: "No",
              value: "2",
            },
          ],
        },
        {
          name: "hasGSTIN",
          label: "4.3 Do you have GSTIN ?",
          type: "radio",
          placeholder: null,
          validation: {
            required: false,
          },
          conditional: true,
          options: [
            {
              text: "Yes",
              value: "1",
            },
            {
              text: "No",
              value: "2",
            },
            {
              text: "Exempted / छूट प्राप्त",
              value: "3",
            },
          ],
        },
      ],
    },
  ],
} as const
