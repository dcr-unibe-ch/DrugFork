# Dataset Metadata: Agency-specific helpful Findings
---

## Contents

- [Overall](#overall)
  - [Definition Public Assessment Report (PAR)](#definition-public-assessment-report-par)
  - [Notice on downloading regulatory documents](#notice-on-downloading-regulatory-documents)
- [PAR based Agencies](#par-based-agencies)
  - [EMA – European Medicines Agency](#-ema--european-medicines-agency)
  - [Swissmedic – Swiss Agency for Therapeutic Products](#-swissmedic--swiss-agency-for-therapeutic-products)
  - [TGA – Therapeutic Goods Administration (Australia)](#-tga--therapeutic-goods-administration-australia)
  - [PMDA – Pharmaceuticals and Medical Devices Agency (Japan)](#-pmda--pharmaceuticals-and-medical-devices-agency-japan)
- [API based Agencies](#api-based-agencies)
  - [FDA – U.S. Food and Drug Administration](#-fda--us-food-and-drug-administration-united-states)
  - [Health Canada – Health Products and Food Branch](#-health-canada--health-products-and-food-branch-canada)


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
(EMA), Health Canada and the Therapeutic Goods Administration (TGA). We therefore recommend limiting
request rates, introducing delays between downloads, and complying with the
respective website terms of use.

### Overview of regulatory agencies and public data characteristics

| Agency | Public assessment reports | Main data granularity | Coverage of generics / biosimilars | Post-authorisation changes | Special characteristics / notes |
|------|---------------------------|-----------------------|------------------------------------|----------------------------|--------------------------------|
| **EMA** | EPAR (systematic) | Product / substance | Yes (included in EPARs) | Integrated into updated EPARs | EPARs are living documents that are updated over time to reflect major regulatory changes |
| **Swissmedic** | SwissPAR (selective) | Substance (initial approval) | No | Selective, only if SwissPAR exists | SwissPARs are static and not updated after publication |
| **TGA** | AusPAR (selective) | Product / substance | Rare, discretionary | Discretionary, not systematic | AusPAR publication depends on application type and TGA discretion |
| **PMDA** | Review Reports (selective) | Product / substance | Rare | Selective for major changes | English translations are provided for reference only; Japanese originals are authoritative |
| **FDA** | No PARs | Submission / application | Yes (explicit NDA / ANDA) | Fragmented across datasets | Regulatory information is distributed across multiple heterogeneous data sources |
| **Health Canada** | No PARs | Submission-like (Drug_code) | Yes | Implicit, via multiple records | Regulatory decisions are represented by Drug_code without explicit submission identifiers |


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

**Additional reports**: EMA does not publish supplementary reports for additional indications (= indication extension) as they implement such updates in the regular EPAR.

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
| Under non-clinical aspects | Non_clinical_abridged |
| Under non-clinical aspects (not always clear) | Referral / Referral body |
| Implicit in text | Drug_class |
| Implicit in text | Disease_class(es) |
| Non-clinical aspects (Pharmacology, Pharmacokinetics, Toxicology) | Animal species, strain, model, sex, in vitro |


## 🇨🇭 **Swissmedic** – Swiss Agency for Therapeutic Products 
---

### Data Sources
Swissmedic publishes regulatory assessment information primarily through Swiss Public
Assessment Reports (SwissPARs). SwissPARs are publicly available via the Swissmedic
website and provide summaries of the scientific and regulatory evaluation
supporting selected marketing authorisation decisions. In addition, Swissmedic
publishes structured information on authorised medicinal products in downloadable
Excel lists. However, these lists do not contain the same level of detail as SwissPARs.

Download SwissPARs: https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/swisspar.html

Download Excel Sheet: https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx


### Scope of published information
**Timeline**: Swissmedic publishes SwissPARs since 2019. PARs do not get revised after
publication, except drugs are no longer authorised (marking on page).

**Substance Types**: Only New Active Substances get SwissPARs, there are no PARs for 
biosimilars or generics. 

**Additional reports**: Review reports for indication extensions or other post-authorisation changes are published selectively and only if a SwissPAR exists for the product.

**Decision Types**: approved, conditional marketing authorisation, refused

**Non clinical experiments**: summary of conducted experiments, not comprehensive. Species,
strain and model are not consistently reported. 


### Granularity of the data  
Swissmedic public data are primarily available at the substance level, as each
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
| Nonclinical aspects: “Swissmedic has not assessed the primary data” | Non_clinical_abridged |
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

**Additional reports**: Major variations in indications or use, are not routinely accompanied by
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
| Under Nonclinical: no (new) experiments have been conducted | Non_clinical_abridged |
| Implicit from text | Drug_class |
| Implicit from text | Disease_class(es) |
| Under Nonclinical (Pharmacology / Pharmacodynamic, Pharmacokinetic, Toxicology) | Animal species, strain, model, sex, in vitro |


## 🇯🇵 **PMDA** – Pharmaceuticals and Medical Devices Agency (Japan)
---

### Data Sources
The Pharmaceuticals and Medical Devices Agency (PMDA) publishes regulatory assessment
information primarily through publicly available review reports and summary documents
for approved medicinal products. These documents are accessible via the PMDA website
and provide descriptions of the scientific and regulatory evaluation supporting marketing
authorisation decisions in Japan. PMDA publishes English translations of selected review reports 
for reference purposes only. These translations are provided for convenience, and the 
original Japanese documents remain authoritative. English versions are available primarily for
recently approved drugs with new active ingredients, selected based on novelty and regulatory
priority.

Download review reports: https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html

### Scope of published information
**Timeline**: Public review reports have been published consistently since 2007, with increasing
availability and standardisation over time. Reports are static documents and are generally not
updated after publication.

**Substance Types**: PMDA review reports are published mainly for new active substances
and selected innovative products. Biosimilars and generics are typically not covered
by detailed public assessment reports. 

**Additional reports**: In some cases, PMDA also publishes review reports for major post
authorisation changes, such as indication extensions or new strengths, particularly when these 
are considered scientifically significant.

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
| Non-proprietary name | Non_proprietary_name |
| Applicant | Marketing_authorisation_holder |
| Dosage form | Pharmaceutical_form |
| Not consistently reported; often embedded in text | Administration_route |
| Results of deliberation | Decision |
| Results of deliberation; if unavailable, document date (top right) | Decision_date |
| Public review reports are generally available only for authorised drugs | Current_status |
| Items warranting special mention | Orphan_drug_status |
| Indication section; additions indicated by underlined text | Indication_extended |
| Indication | Indication_approved |
| Date of application | Application_date |
| Section 3: Non-clinical data (reported per category) | Non_clinical_abridged |
| Implicit from text | Drug_class |
| Implicit from text | Disease_class(es) |
| Section 3: Non-clinical data — (i) Pharmacology, (ii) Pharmacokinetics, (iii) Toxicology | Animal species, strain, model, sex, in vitro |

# API based Agencies
---

## 🇺🇸 **FDA** – U.S. Food and Drug Administration (United States)
---

### Data Sources
The U.S. Food and Drug Administration (FDA) provides public regulatory information
through multiple structured data sources rather than a single consolidated dataset.
Key sources include the openFDA API, downloadable data files from Drugs@FDA, and
auxiliary datasets related to specific regulatory designations (ex. orphan drug status). Each source captures different aspects of the regulatory process and differs in scope and granularity.

**openFDA**
- openFDA provides programmatic access to selected, machine-readable FDA datasets, primarily designed for automated retrieval of labels and structured regulatory metadata.
- Application Number fomat: NDAXXXXX / ANDAXXXXX
- `drug-label-0001-of-0013.json`: structured drug label information  
- `drugs-drugsfda-0001-of-0001.json`: application-level approval metadata
- Link: https://open.fda.gov/
- Information about Drug label API: https://open.fda.gov/apis/drug/label/?utm_source=chatgpt.com

**Drugs@FDA downloadable files (ZIP-folder)**
- Drugs@FDA is the FDA’s primary public repository for drug approval information, presenting application-level records of authorised medicines.
- Application number format: XXXXX (without NDA or ANDA before the number!)
- Drugs@FDA: https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm
- Download Drugs@FDA TXT files: https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files 

**Drugs@FDA TXT files – internal structure**
Applications.txt
│
├── Submissions.txt
│     ├── SubmissionClass_Lookup.txt
│     ├── SubmissionPropertyType.txt
│     ├── Join_Submission_ActionTypes_Lookup.txt
│     │     └── ActionTypes_Lookup.txt
│
├── ApplicationDocs.txt
│     └── ApplicationsDocsType_Lookup.txt
│
└── Products.txt
      ├── MarketingStatus.txt
      │     └── MarketingStatus_Lookup.txt
      └── TE.txt

-> Files can be linkes with common ApplNo

**Additional sources**
- `Orphan_Drug_Status_FDA.xls`: orphan drug designation and approval information  
  (note: application numbers are not consistently provided and may require linkage
  via other identifiers or the FDA API
- Download: https://www.accessdata.fda.gov/scripts/opdlisting/oopd/index.cfm  

### Scope of published information
**Timeline**: FDA data cover a wide historical range, with availability varying by
source and product type. Datasets are updated asynchronously across sources.

**Substance Types**: FDA sources include innovator products, generics, and products
approved via different regulatory pathways. Application types are explicitly
identifiable (e.g. NDA vs ANDA in application number).

**Decision Types**: Initial approvals are consistently reported across FDA data
sources, whereas post-approval regulatory actions (e.g. supplements, label changes,
or discontinuations) are distributed across multiple datasets and are not captured in
a uniform or comprehensive manner.

**Non-clinical experiments**: Public FDA datasets do not provide a unified,
comprehensive non-clinical assessment comparable to PAR documents. Selected sources
contain abbreviated or indirect non-clinical information. (Can be found in Drugs@fda, the name of those documents is not uniform, usually calles Pharamcology/ Toxicology/ Nonclinical review or a combination of such)

### Granularity of the data
FDA public data are frequently available at the submission/application level, with
multiple records per substance reflecting different applications (e.g. NDAs and ANDAs)
and regulatory actions over time. 

### Key identifiers
FDA sources commonly include:
- application numbers (e.g. NDAXXXXX / ANDAXXXXX),
- the non-proprietary name (INN): substance name,
- the product (brand) name.

### Coverage of key variables by FDA data source

| Document | Drug_name | Non_proprietary_name | Marketing_authorisation_holder | Pharmaceutical_form | Administration_route | Decision | Decision_date | Indication | Current_status |
|--------|-----------|----------------------|-------------------------------|---------------------|----------------------|----------|---------------|------------|----------------|
| `drug-label-0001-of-0013.json` (openFDA) | Yes | Yes | No | No | Yes | No | No | Yes | No |
| `drugs-drugsfda-0001-of-0001.json` (openFDA) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | No |
| `MarketingStatus.txt` (Drugs@FDA ZIP) | No | No | No | No | No | No | No | No | Yes |
| `Products.txt` (Drugs@FDA ZIP) | Yes | Yes | No | Yes | Yes | No | No | No | No |
| `Orphan_Drug_Status_FDA.xls` | Yes | Yes | No | No | No | Yes (approved only) | Yes | No | No |


### Coverage of extended regulatory information

| Document | Indication_requested | Non_clinical_abridged | Non-clinical pharmacology | Non-clinical pharmacokinetics | Non-clinical toxicology | Orphan_drug_status | Application_date |
|--------|----------------------|-----------------------|----------------------------|-------------------------------|------------------------|-------------------|------------------|
| `drug-label-0001-of-0013.json` (openFDA) | No | No | Yes (abridged) | No | No | No | No |
| `drugs-drugsfda-0001-of-0001.json` (openFDA) | No | Yes | No | No | No | No | No |
| `MarketingStatus.txt` | No | No | No | No | No | No | No |
| `Products.txt` | No | No | No | No | No | No | No |
| `Orphan_Drug_Status_FDA.xls` | No | No | No | No | No | Yes | No |

Drug_class and Disease_class(es): implicit information, not stated directly in the documents


## 🇨🇦 **Health Canada** – Health Products and Food Branch (Canada)
---

### Data Sources
Health Canada provides publicly accessible regulatory information primarily through the
Drug Product Database (DPD) and associated Product Monographs. The DPD offers
structured records of authorised medicines in Canada and is distributed as a set of
relational text files that can be linked via a shared internal identifier
(Drug_code). Product monographs provide complementary information on
indications, dosing, and safety. In contrast to PAR-based agencies, Health Canada does
not systematically publish public assessment reports for all approvals.
Structured DPD data are available as downloadable text files (ZIP archive, called allfiles),
which together represent regulatory decision records rather than a single consolidated
product list.

Access DPD: https://health-products.canada.ca/dpd-bdpp/ 

Download DPD / data extracts: http://www.hc-sc.gc.ca/dhp mps/prodpharma/databasdon/dpd_bdpp_data_extract-eng.php  

DPD data extract documentation: https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html  

### Scope of published information
**Timeline**: Public availability depends on DPD coverage and the availability of
product monographs; content, structure, and completeness vary over time.

**Substance Types**: The DPD includes a broad range of applications, including new active
substances, biosimilars and generics. Distinguishing them is not possible from a single field and
may require triangulation across multiple DPD files and monograph content.

**Decision Types**: The DPD reflects applications that are approved, marketed or cancelled and since
2017 dormant products. Information on refused or withdrawn submissions is not systematically
captured in a centralised or standardised manner.

**Non-clinical experiments**: Non-clinical data are not consistently published. Since
2019, Health Canada has implemented a legal framework for the public release of
regulatory data; however, the Public Release of Clinical Information (PRCI) portal
covers clinical data only and does not include non-clinical study reports.  
Non-clinical information corresponding to CTD Module 4 (Nonclinical Study Reports /
Summaries) is generally not publicly available. Limited toxicology information may be
found in rare cases at the end of product monographs, accessible via the DPD, but this
is not systematic.

PRCI portal (clinical data only): https://clinical-information.canada.ca/search/ci-rc 

### Granularity of the data
Although Health Canada does not expose explicit submission identifiers comparable to FDA
NDAs or ANDAs, DPD records operate at a submission-like level. Each Drug_code
represents a distinct regulatory decision record, and often multiple Drug_code entries
exist for the same product, reflecting separate approvals for different strengths,
formulations, manufacturers, or other regulatory changes. As a result, Health Canada
public data are more granular than product-level listings but lack an explicit,
standardised submission hierarchy.

### Structure of DPD data extracts
All core DPD text files share the internal identifier Drug_code, which enables
relational linking across datasets. Key files capture drug identity, formulation,
route of administration, regulatory status, and therapeutic classification. The data
represent individual regulatory decisions associated with marketed products rather
than unique substances or products.

**Health Canada DPD – file structure (allfiles)**

drug.txt
│
├── comp.txt
├── ingred.txt
├── form.txt
├── route.txt
├── status.txt
├── ther.txt
├── pharm.txt
├── biosimilar.txt
├── vet.txt
└── package.txt

More detailed information in the Read Me file: https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html

### Key identifiers
Health Canada sources commonly include:
- the Drug Identification Number (DIN),
- an internal Drug_code linking all DPD text files,
- the international non-proprietary name (INN): substance name,
- the product (brand) name.

### Additional considerations
Health Canada does not currently have a formal orphan drug designation system
comparable to the othe regulatory agencies. Orphan drug status is therefore not represented as a
structured field in the DPD, although regulatory initiatives in this area have been
introduced in recent years.

Information on orphan drug policy developments:
https://capra.ca/en/blog/rare-diseases-and-orphan-drugs-regulatory-framework-in-canada-recent-initiatives-by-government-of-canada-2023-05-15
