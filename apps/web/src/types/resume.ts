export interface ContactItem {
  label: string
  value: string
  href?: string
}

export interface EducationItem {
  school: string
  degree: string
  period: string
  note?: string
}

export interface ExperienceItem {
  title: string
  bullets: string[]
}

export interface ProfileInfo {
  nameZh: string
  nameEn: string
  contacts: ContactItem[]
}

export interface ReferenceInfo {
  name: string
  role: string
  email: string
  phone: string
}

export interface AutobiographySection {
  heading: string
  paragraphs: string[]
}

export interface EnglishSection {
  heading: string
  paragraphs?: string[]
  bullets?: string[]
}

export interface ResumeData {
  profile: ProfileInfo
  education: EducationItem[]
  tools: string[]
  experiences: ExperienceItem[]
  strengths: string[]
  reference: ReferenceInfo
  autobiography: AutobiographySection[]
  english: EnglishSection[]
}
