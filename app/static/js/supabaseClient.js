import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = window.__SUPABASE_URL__;
const SUPABASE_ANON_KEY = window.__SUPABASE_ANON_KEY__;

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);