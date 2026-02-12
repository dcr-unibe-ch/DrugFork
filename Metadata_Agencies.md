# Dataset Metadata: Agency-specific helpful Findings
---

## Overall
---

### Definition Public Assessment Report (PAR)
A Public Assessment Report is an official document published by a regulatory
authority that summarizes the scientific evaluation and regulatory reasoning underlying
a decision on the authorization of a medicinal product.
It typically describes the assessment of quality, safety, and efficacy data, outlines
the benefit–risk evaluation, and explains the grounds for approval, refusal, or modification
of a marketing authorization.
PARs are intended to enhance transparency of regulatory decision-making while excluding
confidential commercial information. The exact naming terminology differs between the agencies:
Swissmedic: SwissPAR, EMA: EPAR, TGA: AusPAR, PMDA: Review Report.

TO DO

# PAR based Agencies
---


## 🇪🇺 **EMA** – European Medicines Agency
---

TO DO


## 🇨🇭 **Swissmedic** – Swiss Agency for Therapeutic Products 
---

### Data Sources
Swissmedic organises their data in SwissPARs (=Public Assessment Reports) and also
providesa comprehensive excel sheet (only available in german and french) with all 
currently approved medicines in Switzerland.
Download SwissPARs: https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/swisspar.html
Download Excel Sheet: https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx


### Scope of published information
**Timeline**: Swissmedic publishes SwissPARs since 2019. PARs do not get revised after
publication, except drugs are no longer authorised (marking on page).
**Substance Types**: Only New Active Substances get SwissPARs, there are no PARs for 
biosimilars or generics. Swissmedic also publishes supplementary reports for additional 
indications (= indication extension) if a SwissPAR has been published in the first place. 
**Decision Types**: approved, conditional marketing authorisation, refused
**Non clinical experiments**: summary of conducted experiments, not comprehensive. Species,
strain and model are not consistently reported. 


### Granularity of the data  
Swissmedic public data are primarily available at the **substance level**, as each
SwissPAR generally corresponds to a specific active substance and indication at the
time of first authorisation. Submission-level regulatory actions are not publicly
documented in a systematic manner.


### Key identifiers  
SwissPARs generally include:
- the international non-proprietary name (INN): substance name,
- the product (brand) name,
- the marketing authorisation number (Swissmedic specific)


### Structure of SwissPAR

| Name SwissPAR | Name DrugFork Dataset |
|--------------|-----------------------|
| Marketing authorisation no. | Marketing_authorisation_number |
| Stated on the first page after Swiss Public Assessment report | Drug_name |
| International non-proprietary name | Non_proprietary_name |
| Current Marketing Authorisation Holder | Marketing_authorisation_holder |
| Pharmaceutical form | Pharmaceutical_form |
| Route(s) of administration | Administration_route |
| In table “Regulatory History” line Decision | Decision |
| In table “Regulatory History” line Final decision | Decision_date |
| Default: authorised, if not stated in the text | Current_status |
| Applicant’s request(s), Orphan drug status | Orphan_drug_status |
| Stated in the text | Indication_extended |
| Indication and Dosage, Approved indication | Indication_approved |
| Indication and Dosage, Requested indication | Indication_requested |
| In table “Regulatory History” line Application | Application_date |
| Nonclinical aspects: “Swissmedic has not assessed the primary data” | Non_clinical_abridge |
| Nonclinical aspects, in text | Referral / Referral_body |
| Implicit, in text | Drug_class |
| Implicit, in text | Disease_class(es) |
| Nonclinical aspects (Pharmacology / PK) | Animal species, model, in vitro |


## 🇦🇺 **TGA** – Therapeutic Goods Administration (Australia)
---

TO DO


## 🇯🇵 **PMDA** – Pharmaceuticals and Medical Devices Agency (Japan)
---

TO DO


API based Agencies
---

## 🇺🇸 **FDA** – U.S. Food and Drug Administration
---

TO DO


## 🇨🇦 **Health Canada** – Canadian regulatory authority
---

TO DO


