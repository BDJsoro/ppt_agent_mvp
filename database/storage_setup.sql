-- 1. 'templates' 라는 이름의 새 프라이빗 스토리지 버킷 생성
-- (public = false 로 설정하여 인터넷에 무단 노출 방지)
INSERT INTO storage.buckets (id, name, public) 
VALUES ('templates', 'templates', false);

-- 2. 스토리지 객체(파일)에 대한 RLS(Row Level Security) 접근 제어 활성화
-- (파일 업로드, 조회, 삭제 권한을 오직 '파일의 주인(user_id)'에게만 부여)

-- A. 파일 업로드 정책 (본인의 고유 폴더 안에만 파일 생성 가능)
CREATE POLICY "본인 템플릿만 업로드 가능"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'templates' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- B. 파일 조회 정책 (본인이 올린 파일만 다운로드/보기 가능)
CREATE POLICY "본인 템플릿만 조회 가능"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'templates' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- C. 파일 삭제 정책 (본인이 올린 파일만 삭제 가능)
CREATE POLICY "본인 템플릿만 삭제 가능"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'templates' 
  AND auth.uid()::text = (storage.foldername(name))[1]
);
