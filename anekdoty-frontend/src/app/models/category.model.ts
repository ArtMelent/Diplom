export interface LanguageData {
  language: Language;
  anekdoty: Anekdoty[];
  categories: Categories[];
  tags: Tags[];
}

export interface Language {
  id: number;
  code: string;
  name: string;
  url: string;
}

export interface Categories {
  id: number;
  name: string;
  sub_categories: Categories[];
  language: Language;
  tags: Tags[];
  url: string;
  description: string;
  image_url: string;
  seo_title: string;
  seo_description: string;
  seo_h1: string;
  shown_in_menu: boolean;
  behave_as_tag: boolean;
}

export interface Tags {
  id: number;
  name: string;
  language: Language;
  sub_tags: Tags[];
  description: string;
  seo_title: string;
  seo_description: string;
  seo_h1: string;
  seo_keywords: string;
  breadcrumb: string;
  url: string;
  image_url: string;
  records_per_page: number;
  parsing_words: string;
  slug: string;
  only_subtag: boolean;
}

export interface Anekdoty {
  id: number;
  language: Language;
  Categories: Categories[];
  tags: Tags[];
  h2: string;
  text: string;
  rating: number;
  date_created: string;
  date_modified: string;
}




