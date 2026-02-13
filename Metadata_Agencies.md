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

### Notice on downloading regulatory documents
When downloading regulatory documents at scale, caution is advised. Several agency
websites implement technical safeguards against high request volumes, which may
result in temporary access restrictions, connection resets, or blocking. Such
behaviour was observed in this project particularly for the European Medicines Agency
(EMA) and the Therapeutic Goods Administration (TGA). We therefore recommend limiting
request rates, introducing delays between downloads, and complying with the
respective website terms of use.


TO DO

# PAR based Agencies
---


## 🇪🇺 **EMA** – European Medicines Agency
---

## Data Sources
The European Medicines Agency (EMA) publishes regulatory assessment information
primarily through European Public Assessment Reports (EPARs). EPARs are publicly
available for all centrally authorised medicinal products and can be accessed via
the EMA website. In addition, structured metadata are available through EMA datasets
and downloadable tables, although these are less comprehensive than the EPAR 
documents. EMA also publishes relevant information on the product page, which not 
always matches with the information in the EPARs. 
Download EPARs: https://www.ema.europa.eu/en/search?f%5B0%5D=ema_medicine_bundle%3Aema_medicine&f%5B1%5D=ema_search_categories%3A83
Information about EPARS: https://www.ema.europa.eu/en/medicines/what-we-publish-medicines-when/european-public-assessment-reports-background-context
Medicine information tables: https://www.ema.europa.eu/en/medicines/download-medicine-data


## Scope of published information
**Timeline**: EPARs have been published since the establishment of the centralised
procedure in 1995. EPARs are updated over time to reflect major regulatory changes,
such as new indications, variations, or safety-related updates.
**Substance Types**: EMA publishes EPARs for every medicine that has been approved or refused. Which means that not only new active substances, but also generics and biosimilars get EPARs.
**Additional reports** EMA does not publish supplementary reports for additional indications (= indication extension) as they implement such updates in the regular EPAR.
**Decision Types**: approved, conditional marketing authorisation, withdrawn, refused
**Non clinical experiments**: EPARs typically summarise non-clinical pharmacology,
pharmacokinetics, and toxicology data. The level of detail varies across reports and
over time; experimental species, models and strains are often mentioned but not reported in a
systematic or standardised manner. The reports are much more detailed than SwissPARs.


### Granularity of the data  
EMA public data are primarily available at the substance and product level.
Each EPAR corresponds to a centrally authorised medicinal product and documents the
initial authorisation as well as subsequent major regulatory changes. Individual
submissions and variations are not provided as standalone, submission-level records
but are integrated into the evolving EPAR documents.


### Key identifiers  
EPARs generally include:
- the international non-proprietary name (INN): substance name,
- the product (brand) name,
- a document nuber for each EPAR,
- the EMA product number (drug-specific).

### Structure of EPAR

| Name EPAR | Name DrugFork Dataset |
|----------|-----------------------|
| Document number (first page, top left, starts with EMA/) | Marketing_authorisation_number |
| Procedure no. (first page) | EMA_product_number |
| Stated on the first page after Assessment Report | Drug_name |
| International non-proprietary name | Non_proprietary_name |
| Submission of the dossier (in text) | Marketing_authorisation_holder |
| About the product (in text) | Pharmaceutical_form |
| About the product (in text) | Administration_route |
| Steps taken for the assessment of the product (table) | Decision |
| Steps taken for the assessment of the product (table) | Decision_date |
| Not directly stated; default for approved drugs: authorised | Current_status |
| Submission of the dossier (in text, if applicable) | Orphan_drug_status |
| In text, if applicable | Indication_extended |
| Recommendations, Outcome | Indication_approved |
| Submission of the dossier (in text: applicant applied for the following indication) | Indication_requested |
| Submission of the dossier (in text) | Application_date |
| Under non-clinical aspects | Non_clinical_abridge |
| Under non-clinical aspects (not always clear) | Referral / Referral body |
| Implicit in text | Drug_class |
| Implicit in text | Disease_class(es) |
| Non-clinical aspects (Pharmacology, Pharmacokinetics, Toxicology) | Animal species, strain, model, sex, in vitro |


## 🇨🇭 **Swissmedic** – Swiss Agency for Therapeutic Products 
---

### Data Sources
Swissmedic organises their data in SwissPARs (=Public Assessment Reports) and also
provides a comprehensive excel sheet (only available in german and french) with all 
currently approved medicines in Switzerland.
Download SwissPARs: https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/swisspar.html
Download Excel Sheet: https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx


### Scope of published information
**Timeline**: Swissmedic publishes SwissPARs since 2019. PARs do not get revised after
publication, except drugs are no longer authorised (marking on page).
**Substance Types**: Only New Active Substances get SwissPARs, there are no PARs for 
biosimilars or generics. 

**Additional reports** Review reports for indication extensions or other post-authorisation changes are published selectively and only if a SwissPAR exists for the product.

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
- the marketing authorisation number (Swissmedic specific).


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

### Data Sources
The Therapeutic Goods Administration (TGA) publishes regulatory assessment information
primarily through Australian Public Assessment Reports (AusPARs). AusPARs are publicly
available via the TGA website in PDF and Word format and provide summaries of
the scientific and regulatory evaluation supporting the approval of selected
prescription medicines. 
In addition, the TGA publishes several structured datasets in CSV format, including 
Cognos exports (e.g. cognos_v_gen), which contain extensive regulatory metadata. However, 
these datasets do not share a single consistent primary identifier across
files, requiring cross-referencing of multiple identifiers (e.g. ARTG numbers,
product IDs, or submission-related fields) to link information between datasets and
with AusPAR documents.

Download AusPARs: https://www.tga.gov.au/resources/australian-public-assessment-reports-auspar

Information AusPARs: https://www.tga.gov.au/products/regulations-all-products/about-australian-register-therapeutic-goods-artg/about-australian-public-assessment-reports-prescription-medicines-auspars

Information submission types: https://www.tga.gov.au/resources/guidance/understanding-australian-public-assessment-reports-auspars-prescription-medicines

Download csv documents: https://apps.tga.gov.au/downloads/

### Scope of published information
**Timeline**: AusPARs have been published since 2009. Reports are static documents and
are generally not updated after publication. 

**Substance Types**: AusPARs are published primarily for new active substances (Type A) and new fixed combination medicines (Type B). Other application types, including biosimilars and 
generics are not routinely accompanied by AusPARs and may be published at the discretion of the TGA.

**Additional reports** Major variations in indications or use, are not routinely accompanied by
AusPARs and may be published at the discretion of the TGA.

**Decision Types**: approved, withdrawn, rejected, refused.

**Non-clinical experiments**: AusPARs summarise non-clinical pharmacology,
pharmacokinetics, and toxicology data. The reporting of experimental species, models,
and study details is variable and not standardised across reports. This information is not available in the structured datasets.

### Granularity of the data
TGA public data provided through AusPARs are primarily available at the substance
and product level, typically corresponding to the initial approval of a medicinal
product. Submission-level regulatory actions and post-approval variations are not
systematically documented in public sources. TGA Cognos datasets provide more fine-grained, structured regulatory metadata than public assessment reports, although they do not represent full submission-level histories comparable to FDA or Health Canada APIs.

### Key identifiers
AusPARs generally include:
- the international non-proprietary name (INN): substance name,
- the product (brand) name,
- the Australian Register of Therapeutic Goods (ARTG) number,
- the document number (in document name).

### Structure of AusPAR

| Name AusPAR | Name DrugFork Dataset |
|-------------|-----------------------|
| Number in document name (not in text) | Marketing_authorisation_number |
| Product name | Drug_name |
| Active ingredient | Non_proprietary_name |
| Sponsor’s name and address (first line only) | Marketing_authorisation_holder |
| Dose form | Pharmaceutical_form |
| Route of administration | Administration_route |
| Decision | Decision |
| Date of withdrawal / Date of approval | Decision_date |
| Not reported | Current_status |
| In table “Timeline for Submission”: first line “Positive Designation (Orphan)”; in older reports stated in text | Orphan_drug_status |
| If type of submission: Extension of indications = yes | Indication_extended |
| Approved therapeutic use | Indication_approved |
| In text, mostly under “Product background” | Indication_requested |
| In table “Timeline for Submission”: submission dossier accepted | Application_date |
| Under Nonclinical: no (new) experiments have been conducted | Non_clinical_abridge |
| Implicit from text | Drug_class |
| Implicit from text | Disease_class(es) |
| Under Nonclinical (Pharmacology / Pharmacodynamic, Pharmacokinetic, Toxicology) | Animal species, strain, model, sex, in vitro |


## 🇯🇵 **PMDA** – Pharmaceuticals and Medical Devices Agency (Japan)
---

### Data Sources
The Pharmaceuticals and Medical Devices Agency (PMDA) publishes regulatory assessment
information primarily through publicly available review reports and summary documents
for approved medicinal products. These documents are accessible via the PMDA website
and provide descriptions of the scientific and regulatory evaluation supporting marketing authorisation decisions in Japan. PMDA publishes English translations of selected review reports 
for reference purposes only. These translations are provided for convenience, and the 
original Japanese documents remain authoritative. English versions are available primarily for recently approved drugs with new active ingredients, selected based on novelty and regulatory
priority.

Download review reports: https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html

### Scope of published information
**Timeline**: Public review reports have been published consistently since 2007, with increasing availability and standardisation over time. Reports are static documents and are generally not updated after publication.

**Substance Types**: PMDA review reports are published mainly for new active substances
and selected innovative products. Biosimilars and generics are typically not covered
by detailed public assessment reports. 

**Additional reports** In some cases, PMDA also publishes review reports for major post-authorisation changes, such as indication extensions or new strengths, particularly when these are considered scientifically significant.

**Decision Types**: approved; information on refused or withdrawn applications is not systematically published.

**Non-clinical experiments**: Review reports summarise non-clinical pharmacology,
pharmacokinetics, and toxicology data. Reporting of experimental species, models, and
study details is variable and not fully standardised. 

### Granularity of the data
PMDA public regulatory information is primarily available at the substance and
product level, reflecting individual marketing authorisation decisions. Detailed
submission-level histories, including supplements or post-authorisation variations,
are not systematically available in public datasets.

### Key identifiers
PMDA review reports generally include:
- the international non-proprietary name (INN): substance name,
- the product (brand) name,
- the marketing authorisation holder,
- PMDA- or MHLW-specific approval identifiers.

### Structure of PMDA Review Report
| Name Japan PAR | Name in Google Sheets |
|----------------|-----------------------|
| Document number (without leading zero; not explicitly stated in text) | Marketing authorisation number |
| Brand name | Drug |
| Non-proprietary name | Non proprietary name |
| Applicant | Marketing authorisation holder |
| Dosage form | Pharmaceutical form |
| Not consistently reported; often embedded in text | Administration route |
| Results of deliberation | Decision |
| Results of deliberation; if unavailable, document date (top right) | Decision date |
| Public review reports are generally available only for authorised drugs | Current status |
| Items warranting special mention | Orphan drug status |
| Indication section; additions indicated by underlined text | Indication extended |
| Indication | Indication approved |
| Date of application | Application date |
| Not reported | Number of decisions |
| Section 3: Non-clinical data (reported per category) | Non clinical abridge |
| Usually not reported | Referral / Referral body |
| Implicit from text | Drug class |
| Implicit from text | Disease class |
| Section 3: Non-clinical data — (i) Pharmacology, (ii) Pharmacokinetics, (iii) Toxicology | Animal species, strain, model, sex, in vitro |

# API based Agencies
---

## 🇺🇸 **FDA** – U.S. Food and Drug Administration
---

TO DO


## 🇨🇦 **Health Canada** – Canadian regulatory authority
---

TO DO


