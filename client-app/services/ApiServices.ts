import axios from 'axios';
import type { Settings, PromptInfo, Prompt } from '~/types/Schemas';

const config = useAppConfig();
const API_BASE_URL = `${config.apiBaseUrl}/api`;

axios.defaults.baseURL = API_BASE_URL;
axios.defaults.headers.post['Content-Type'] = 'application/json';

export class SettingsService {
  async getSettings(): Promise<Settings> {
    const response = await axios.get('/settings/');
    return response.data;
  }

  async updateSetting(key: string, value: string | number): Promise<boolean> {
    const response = await axios.post('/settings/', {
      key,
      value: (typeof value === 'number') ? value.toString() : value,
    });
    if (response.status === 200) {
      return true;
    }
    return false;
  }
}

export class PromptsService {
  async getPromptTemplates(): Promise<PromptInfo[]> {
    const response = await axios.get('/prompts/templates');
    return response.data;
  }

  async getPromptTemplate(template_id: string): Promise<Prompt> {
    const response = await axios.get(`/prompts/templates/${template_id}`);
    return response.data;
  }

}
