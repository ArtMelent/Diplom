import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Language, LanguageData } from '../models/category.model';
import { CategoryDefaultService } from '../services/category-default.service';
import { LanguageService } from '../services/language.service';
import { AutoLinkPipe } from '../pipes/auto-link.pipe';

@Component({
  selector: 'app-language',
  templateUrl: 'language.component.html',
  styleUrls: ['language.component.scss'],
  // providers: [AutoLinkPipe],
})
export class LanguageComponent implements OnInit {
  languageData: LanguageData[] = [];
  constructor(
    private route: ActivatedRoute,
    private categoryService: CategoryDefaultService,
    private languageService: LanguageService,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const langUrl = params.get('langUrl');
      console.log('langUrl:', langUrl);
      if (langUrl) {
        const language: Language = { id: 0, code: '', name: '', url: langUrl };
        this.fetchLanguageData(language);
      }
    });
  }

  fetchLanguageData(language: Language): void {
    this.categoryService.getLanguageDataByUrl(language).subscribe({
      next: (data: LanguageData) => {
        this.languageData = [data];
        language.id = data.language.id; // Update the language ID
        language.code = data.language.code; // Update the language code
        language.name = data.language.name; // Update the language name
        this.languageService.setSelectedLanguage(language); // Set the selected language
      },
      error: (error) => {
        console.error(error);
      }
    });
  }
}
