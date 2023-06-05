import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { tap } from 'rxjs';
import { LanguageData, Language, Categories, Tags, Anekdoty } from '../models/category.model';
import { CategoryDefaultService } from '../services/category-default.service';
import { LanguageService } from '../services/language.service';
import { AutoLinkPipe } from '../pipes/auto-link.pipe';

@Component({
  selector: 'app-subcategory',
  templateUrl: './subcategory.component.html',
  styleUrls: ['./subcategory.component.scss'],
  providers: [AutoLinkPipe]
})
export class SubcategoryComponent implements OnInit {
  langUrl!: string;
  categoryUrl!: string;
  subcategoryUrl!: string;
  categoryData: Categories | null = null;
  languageData: LanguageData[] = [];
  subcategoryData: Categories | null = null;
  commonTags: Tags[] = [];
  records: Anekdoty[] = [];

  constructor(
    private route: ActivatedRoute,
    private categoryService: CategoryDefaultService,
    private languageService: LanguageService,
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.langUrl = params.get('langUrl') || '';
      this.categoryUrl = params.get('category_url') || '';
      this.subcategoryUrl = params.get('subcategory_url') || '';

      if (this.langUrl) {
        const language: Language = { id: 0, code: '', name: '', url: this.langUrl };
        this.loadCategoryData(language);
      }
    });
  }

  loadCategoryData(language: Language) {
    this.categoryService
      .getCategoryData(this.langUrl, this.categoryUrl, this.subcategoryUrl)
      .pipe(
        tap((data) => {
          this.categoryData = data.category;
          this.subcategoryData = data.subcategory;
          this.commonTags = data.common_tags;
          this.records = data.records;
        })
      )
      .subscribe({
        next: (data: LanguageData) => {
          this.languageData = [data];
          language.id = data.language.id; // Update the language ID
          language.code = data.language.code; // Update the language code
          language.name = data.language.name; // Update the language name
          this.languageService.setSelectedLanguage(language); // Set the selected language
        },
        error: (error) => {
          console.error('Failed to load category data:', error);
        },
      });
  }

  getCategoryUrl(languageUrl: string | undefined, categoryUrl: string | undefined): string {
    if (!languageUrl || !categoryUrl) {
      return ''; // Handle the case when any of the URLs is undefined
    }
    return `/${languageUrl}/${categoryUrl}`;
  }

  getTagUrl(
    languageUrl: string | undefined,
    categoryUrl: string | undefined,
    subcategoryUrl: string | undefined,
    tagUrl: string | undefined
  ): string {
    if (!languageUrl || !categoryUrl || !subcategoryUrl || !tagUrl) {
      return ''; // Handle the case when any of the URLs is undefined
    }
    return `/${languageUrl}/${categoryUrl}/${subcategoryUrl}/${tagUrl}`;
  }
}
