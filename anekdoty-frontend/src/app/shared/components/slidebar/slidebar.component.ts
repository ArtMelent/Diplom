import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LanguageData, Language } from 'src/app/models/category.model';
import { CategoryDefaultService } from 'src/app/services/category-default.service';

@Component({
  selector: 'app-slidebar',
  templateUrl: './slidebar.component.html',
  styleUrls: ['./slidebar.component.scss']
})
export class SlidebarComponent implements OnInit{
  languageData: LanguageData[] = [];

  constructor(
    private route: ActivatedRoute,
    private languageService: CategoryDefaultService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const langUrl = params.get('langUrl');
      if (langUrl) {
        const language: Language = { id: 0, code: '', name: '', url: langUrl };
        this.fetchLanguageData(language);
      }
    });
  }

  fetchLanguageData(language: Language): void {
    this.languageService.getLanguageDataByUrl(language).subscribe({
      next: (data: LanguageData) => {
        this.languageData = [data];
      },
      error: (error) => {
        console.error(error);
      }
    });
  }
}
