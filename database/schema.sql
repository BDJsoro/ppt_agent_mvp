-- 1. 유저 프로필 테이블 (Supabase Auth와 연결)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  updated_at TIMESTAMP WITH TIME ZONE,
  full_name TEXT
);

-- RLS (Row Level Security) 설정
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- 2. 템플릿 및 설정 저장 테이블
CREATE TABLE templates (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  font_name TEXT NOT NULL, -- 예: 'NanumBarunGothic'
  file_path TEXT, -- Storage 내의 원본 PPTX 파일 경로
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 설정
ALTER TABLE templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users manage own templates" ON templates FOR ALL USING (auth.uid() = user_id);

-- 3. 생성 이력 (History) 테이블
CREATE TABLE history (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  topic TEXT NOT NULL,
  slide_count INTEGER NOT NULL,
  template_id UUID REFERENCES templates(id) ON DELETE SET NULL,
  download_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 설정
ALTER TABLE history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users manage own history" ON history FOR ALL USING (auth.uid() = user_id);
