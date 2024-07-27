enum ChatRole {
    USER = 'user',
    ASSISTANT = 'assistant',
    SYSTEM = 'system'
}

interface IChatMessage {
    message: string;
    role: ChatRole;
    generating?: boolean;
}

interface Settings {
    llm_default_model: string;
    llm_temperature: number;
    llm_api_key: string | null;
    llm_endpoint: string;
    llm_ollama_endpoint: string;
    general_theme: "dark" | "light" | "auto";
    general_username: string;
    llm_top_p: number;
    llm_top_k: number;
    llm_seed: number;
}

interface SettingsWrapper {
    settings: Settings;
    isLoading: boolean;
    loaded: boolean;
    error: any;
}

interface PromptInfo {
    id: string;
    name: string;
}

interface Prompt extends PromptInfo {
    prompt: string;
    system_prompt?: string;
    user_input: string;
}

interface Prompts {
    prompts: Prompt[];
}

enum DataSourceType {
    SQLite = "SQLite",
    // DuckDB = "DuckDB",
    // PostgreSQL = "PostgreSQL",
    // MySQL = "MySQL",
    // SQLServer = "SQLServer",
    // Oracle = "Oracle",
    // MongoDB = "MongoDB",
    // Redis = "Redis",
}

interface DataSourceModel {
    id: number; // Optional in TypeScript
    name: string;
    description?: string; // Optional in TypeScript
    type: DataSourceType;
    conn_str: string;
}

// Create model excludes auto-generated fields like 'id'
interface DataSourceCreateModel {
    name?: string;
    description?: string; // Made optional by adding '?'
    type?: DataSourceType | null;
    conn_str?: string;
}

// Update model makes all fields optional
interface DataSourceUpdateModel {
    name?: string;
    description?: string;
    type?: DataSourceType;
    conn_str?: string;
}

interface SchemaTablesModel {
    schema?: string;
    tables: string[];
}

interface ColumnInfoModel {
    name: string;
    primary_key: boolean;
    index?: boolean;
    unique?: boolean;
    data_type: string;
    nullable: boolean;
    default?: string;
    autoincrement?: boolean;
    comment?: string;
}

interface DataProviderInfoModel extends DataSourceModel {
    supports_schema: boolean;
    metadata: SchemaTablesModel[];
}

interface SqlStatementModel {
    sql: string;
}


export { ChatRole, type IChatMessage, type Settings, type PromptInfo, type Prompt, type Prompts, type SettingsWrapper, DataSourceType, type DataSourceModel, type DataSourceCreateModel, type DataSourceUpdateModel, type SchemaTablesModel, type ColumnInfoModel, type DataProviderInfoModel, type SqlStatementModel };
