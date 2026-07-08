// AppDisplay: central display strings and domain label mapping for EN/TH UI.
// How it works: pass AppState (from Provider) — uses AppState.translate for UI copy
// and maps internal/API keys (status codes, body locations, HAM100 labels) to
// localized display text without changing stored or sent values.

import '../app_state.dart';

/// Shared EN/TH display helpers (navigation, filters, charts, domain labels).
class AppDisplay {
  AppDisplay._();

  // --- Bottom navigation ---
  static String navHome(AppState a) => a.translate('Home', 'หน้าแรก');
  static String navDashboard(AppState a) =>
      a.translate('Dashboard', 'แดชบอร์ด');
  static String navNotification(AppState a) =>
      a.translate('Notification', 'การแจ้งเตือน');
  static String navSettings(AppState a) =>
      a.translate('Setting', 'ตั้งค่า');

  // --- Home / case list ---
  static String hiUser(AppState a, String name) =>
      a.translate('Hi, $name', 'สวัสดี $name');
  static String welcomeTagline(AppState a) => a.translate(
        'Welcome to Dermalytix Active',
        'ยินดีต้อนรับสู่ Dermalytix Active',
      );
  static String searchCasesHint(AppState a) => a.translate(
        'Search patient name or ID...',
        'ค้นหาชื่อผู้ป่วยหรือรหัสเคส...',
      );
  static String startNewCaseTitle(AppState a) =>
      a.translate('Start New Case', 'เริ่มเคสใหม่');
  static String startNewCaseDescription(AppState a) => a.translate(
        'Capture patient skin images for diagnosis',
        'ถ่ายภาพผิวหนังผู้ป่วยเพื่อวินิจฉัย',
      );
  static String labelingCaseTitle(AppState a) =>
      a.translate('Labeling Case', 'ป้ายกำกับเคส');
  static String labelingCaseDescription(AppState a) => a.translate(
        'Active learning selection for doctor labeling',
        'เลือกเคสสำหรับการติดป้ายกำกับ (active learning)',
      );
  static String startLabelingCaseButton(AppState a) => a.translate(
        'Start Labeling Case',
        'เริ่มป้ายกำกับเคส',
      );
  static String caseRecord(AppState a) =>
      a.translate('Case record', 'บันทึกเคส');
  static String loadingCases(AppState a) =>
      a.translate('Loading cases...', 'กำลังโหลดเคส...');
  static String couldNotLoadCases(AppState a) =>
      a.translate('Could not load cases', 'โหลดเคสไม่สำเร็จ');
  static String retry(AppState a) => a.translate('Retry', 'ลองอีกครั้ง');
  static String noCasesForDate(AppState a) => a.translate(
        'No cases found for this date',
        'ไม่พบเคสในวันที่เลือก',
      );
  static String noCasesFound(AppState a) =>
      a.translate('No cases found', 'ไม่พบเคส');
  static String tryAnotherDate(AppState a) =>
      a.translate('Try another date', 'ลองเลือกวันอื่น');
  static String tryAdjustFilters(AppState a) => a.translate(
        'Try adjusting your filters or search',
        'ลองปรับตัวกรองหรือคำค้น',
      );
  static String unknownLocation(AppState a) => a.translate(
        'Unknown Location',
        'ตำแหน่งไม่ทราบ',
      );
  static String predictPrefix(AppState a) =>
      a.translate('Predict:', 'คาดการณ์:');
  static String pending(AppState a) =>
      a.translate('Pending', 'รอดำเนินการ');
  static String notAvailable(AppState a) => a.translate('N/A', 'ไม่มีข้อมูล');
  static String unknown(AppState a) =>
      a.translate('Unknown', 'ไม่ทราบ');
  static String amPm(AppState a, bool isPm) =>
      isPm ? a.translate('P.M.', 'บ่าย') : a.translate('A.M.', 'ก่อนบ่าย');

  static String caseStatusFilter(AppState a, String value) {
    switch (value) {
      case 'All':
        return a.translate('All', 'ทั้งหมด');
      case 'Confirmed':
        return a.translate('Confirmed', 'ยืนยันแล้ว');
      case 'Uncertain':
        return a.translate('Uncertain', 'ไม่แน่นอน');
      case 'Rejected':
        return a.translate('Rejected', 'ปฏิเสธ');
      case 'Labeled':
        return a.translate('Labeled', 'ติดป้ายกำกับแล้ว');
      default:
        return value;
    }
  }

  /// Display backend/derived status on case cards (English canonical → TH).
  static String caseRecordStatusChip(AppState a, String statusEnglish) {
    final s = statusEnglish.trim();
    switch (s.toLowerCase()) {
      case 'confirmed':
        return a.translate('Confirmed', 'ยืนยันแล้ว');
      case 'uncertain':
      case 'pending':
        return a.translate('Uncertain', 'ไม่แน่นอน');
      case 'rejected':
        return a.translate('Rejected', 'ปฏิเสธ');
      case 'labeled':
        return a.translate('Labeled', 'ติดป้ายกำกับแล้ว');
      default:
        return s.isEmpty ? a.translate('Unknown', 'ไม่ทราบ') : s;
    }
  }

  // --- Patient type modal (home) ---
  static String selectSkinCondition(AppState a) => a.translate(
        'Select Skin Condition',
        'เลือกสภาพผิว',
      );
  static String selectSkinConditionSubtitle(AppState a) => a.translate(
        'Please Choose the primary condition for this case to guide analysis',
        'โปรดเลือกภาวะหลักของเคสนี้เพื่อช่วยการวิเคราะห์',
      );
  static String skinLesionTitle(AppState a) =>
      a.translate('Skin Lesion', 'รอยผิวหนัง');
  static String skinLesionDescription(AppState a) => a.translate(
        'For evaluating suspicious or changing skin lesions.',
        'สำหรับประเมินรอยผิวที่น่าสงสัยหรือเปลี่ยนแปลง',
      );
  static String create(AppState a) => a.translate('Create', 'สร้าง');

  // --- Calendar ---
  static String calendarToday(AppState a) =>
      a.translate('Today', 'วันนี้');
  static String calendarTitle(AppState a) =>
      a.translate('Calendar', 'ปฏิทิน');
  static String monthShort(AppState a, int month) {
    const keys = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ];
    const th = [
      'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
      'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.',
    ];
    final i = month.clamp(1, 12) - 1;
    return a.translate(keys[i], th[i]);
  }

  static String weekdayShort(AppState a, int weekday) {
    const en = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];
    const th = ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.'];
    final i = weekday.clamp(1, 7) - 1;
    return a.translate(en[i], th[i]);
  }

  // --- Dashboard periods (internal value = English) ---
  static String dashboardPeriod(AppState a, String period) {
    switch (period) {
      case 'Today':
        return a.translate('Today', 'วันนี้');
      case 'This Week':
        return a.translate('This Week', 'สัปดาห์นี้');
      case 'This Month':
        return a.translate('This Month', 'เดือนนี้');
      case 'All Time':
        return a.translate('All Time', 'ตลอดกาล');
      default:
        return period;
    }
  }

  static String chartStackLabel(AppState a, String label) {
    switch (label) {
      case 'Accept':
        return a.translate('Accept', 'ยอมรับ');
      case 'Uncertain':
        return a.translate('Uncertain', 'ไม่แน่นอน');
      case 'Reject':
        return a.translate('Reject', 'ปฏิเสธ');
      case 'No Data':
        return a.translate('No Data', 'ไม่มีข้อมูล');
      default:
        return label;
    }
  }

  /// Month-year keys like "2024-01" → short localized label.
  static String dashboardMonthYearKey(AppState a, String key) {
    final parts = key.split('-');
    if (parts.length == 2) {
      final y = int.tryParse(parts[0]);
      final m = int.tryParse(parts[1]);
      if (y != null && m != null && m >= 1 && m <= 12) {
        return '${monthShort(a, m)} $y';
      }
    }
    return key;
  }

  static String weekOfMonth(AppState a, String wKey) {
    if (wKey.startsWith('W') && wKey.length > 1) {
      return a.translate(wKey, 'สัปดาห์ที่ ${wKey.substring(1)}');
    }
    return wKey;
  }

  // --- Notifications ---
  static String notifFilterAll(AppState a) =>
      a.translate('All', 'ทั้งหมด');
  static String notifFilterNewCases(AppState a) =>
      a.translate('New cases', 'เคสใหม่');
  static String notifFilterPending(AppState a) => a.translate(
        'Pending labeling',
        'รอป้ายกำกับ',
      );
  static String relativeJustNow(AppState a) =>
      a.translate('just now', 'เมื่อสักครู่');
  static String relativeMinutesAgo(AppState a, int m) =>
      a.translate('${m}m ago', '${m} นาทีที่แล้ว');
  static String relativeHoursAgo(AppState a, int h) =>
      a.translate('${h}h ago', '${h} ชม.ที่แล้ว');
  static String relativeDaysAgo(AppState a, int d) =>
      a.translate('${d}d ago', '${d} วันที่แล้ว');

  // --- Login / auth ---
  static String loginHeroTitle(AppState a) => a.translate(
        'Detect skin cancer early cutting edge ML',
        'ตรวจจับมะเร็งผิวหนังเร็วด้วย ML แนวหน้า',
      );
  static String loginHeroSubtitle(AppState a) => a.translate(
        'Capture or upload a skin photo to get an instant\n'
        'AI-based skin analysis and insights for early detection.',
        'ถ่ายหรืออัปโหลดภาพผิวเพื่อรับการวิเคราะห์ด้วย AI\n'
        'และข้อมูลเชิงลึกเพื่อการคัดกรองเร็ว',
      );
  static String enterUsername(AppState a) =>
      a.translate('Enter Your Username', 'กรอกชื่อผู้ใช้');
  static String enterPassword(AppState a) =>
      a.translate('Enter Your Password', 'กรอกรหัสผ่าน');
  static String rememberMe(AppState a) =>
      a.translate('Remember me', 'จดจำฉัน');
  static String forgotPasswordLink(AppState a) =>
      a.translate('Forgot Password?', 'ลืมรหัสผ่าน?');
  static String signIn(AppState a) => a.translate('SIGN IN', 'เข้าสู่ระบบ');
  static String orDivider(AppState a) => a.translate('OR', 'หรือ');
  static String signInWithGoogle(AppState a) => a.translate(
        'Sign in with Google',
        'เข้าสู่ระบบด้วย Google',
      );
  static String enterUsernamePassword(AppState a) => a.translate(
        'Please enter Username and Password',
        'กรุณากรอกชื่อผู้ใช้และรหัสผ่าน',
      );
  static String cannotConnectServer(AppState a) => a.translate(
        'Cannot connect to server. Please check your network.',
        'เชื่อมต่อเซิร์ฟเวอร์ไม่ได้ โปรดตรวจสอบเครือข่าย',
      );
  static String invalidCredentials(AppState a) => a.translate(
        'Invalid Username or Password',
        'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง',
      );
  static String cannotConnectShort(AppState a) => a.translate(
        'Cannot connect to server',
        'เชื่อมต่อเซิร์ฟเวอร์ไม่ได้',
      );
  static String loginFailed(AppState a) => a.translate(
        'Login failed. Please try again.',
        'เข้าสู่ระบบล้มเหลว โปรดลองอีกครั้ง',
      );
  static String googleSignInDisabled(AppState a) => a.translate(
        'Google sign-in is temporarily disabled until OAuth setup is completed.',
        'การเข้าสู่ระบบ Google ปิดชั่วคราวจนกว่าจะตั้งค่า OAuth เสร็จ',
      );

  // --- Forgot password ---
  static String forgotPasswordTitle(AppState a) =>
      a.translate('Forgot Password', 'ลืมรหัสผ่าน');
  static String resetPasswordHeading(AppState a) => a.translate(
        'Reset your password',
        'รีเซ็ตรหัสผ่าน',
      );
  static String resetPasswordSubtitle(AppState a) => a.translate(
        'We will send you a secure link to restore access.',
        'เราจะส่งลิงก์ปลอดภัยเพื่อกู้การเข้าใช้',
      );
  static String emailLabel(AppState a) => a.translate('Email', 'อีเมล');
  static String emailHint(AppState a) =>
      a.translate('name@example.com', 'name@example.com');
  static String emailRequired(AppState a) =>
      a.translate('Email is required', 'กรุณากรอกอีเมล');
  static String emailInvalid(AppState a) => a.translate(
        'Enter a valid email',
        'อีเมลไม่ถูกต้อง',
      );
  static String sendResetLink(AppState a) => a.translate(
        'Send Reset Link',
        'ส่งลิงก์รีเซ็ต',
      );
  static String passwordResetMock(AppState a) => a.translate(
        'Password reset link sent (mock).',
        'ส่งลิงก์รีเซ็ตรหัสผ่านแล้ว (จำลอง)',
      );

  // --- Profile image dialog ---
  static String selectImageSource(AppState a) => a.translate(
        'Select Image Source',
        'เลือกแหล่งที่มาของรูป',
      );
  static String camera(AppState a) =>
      a.translate('Camera', 'กล้อง');
  static String gallery(AppState a) =>
      a.translate('Gallery', 'คลังรูป');
  static String cameraUnavailableMessage(AppState a) => a.translate(
        'Camera not available on this device. Please upload an image instead.',
        'กล้องใช้งานไม่ได้บนอุปกรณ์นี้ โปรดอัปโหลดจากคลังแทน',
      );
  static String errorPickingImage(AppState a, String e) =>
      a.translate('Error picking image: $e', 'เลือกรูปผิดพลาด: $e');
  static String errorDeletingImage(AppState a, String e) =>
      a.translate('Error deleting image: $e', 'ลบรูปผิดพลาด: $e');

  // --- HAM100 / model short codes → display (EN full name in EN mode; TH in TH mode) ---
  static const Map<String, List<String>> _dxCode = {
    'akiec': ['Actinic keratoses', 'เกล็ดเหลืองจากแสงแดด'],
    'bcc': ['Basal cell carcinoma', 'มะเร็งเซลล์ฐาน'],
    'bkl': ['Benign keratosis-like lesions', 'รอยผิวคล้ายเกล็ดที่ไม่เป็นมะเร็ง'],
    'df': ['Dermatofibroma', 'เดอร์มาโตไฟโบรมา'],
    'mel': ['Melanoma', 'มะเร็งผิวหนังชนิดเมลาโนมา'],
    'nv': ['Melanocytic nevi', 'ไฝเม็ดสี'],
    'vasc': ['Vascular lesions', 'รอยแดงหลอดเลือด'],
  };

  static String predictionLabel(AppState a, String? raw) {
    final t = raw?.trim();
    if (t == null || t.isEmpty) {
      return a.translate('Unknown', 'ไม่ทราบ');
    }
    final code = _dxCode[t.toLowerCase()];
    if (code != null) {
      return a.translate(code[0], code[1]);
    }
    // Title-case unknown tokens for display only
    final cleaned = t.replaceAll(RegExp(r'[_-]+'), ' ').trim();
    final words = cleaned.split(RegExp(r'\s+'));
    final titled = words
        .map((w) {
          if (w.isEmpty) return w;
          final lower = w.toLowerCase();
          return '${lower[0].toUpperCase()}${lower.substring(1)}';
        })
        .join(' ');
    return titled;
  }

  // --- Create case: body locations (stored value = English key) ---
  static const List<String> locationKeys = [
    'Front Head',
    'Front Neck',
    'Front Chest',
    'Front Abdomen',
    'Front Left Arm',
    'Front Right Arm',
    'Front Left Forearm',
    'Front Right Forearm',
    'Front Left Hand',
    'Front Right Hand',
    'Front Left Thigh',
    'Front Right Thigh',
    'Front Left Leg',
    'Front Right Leg',
    'Front Left Foot',
    'Front Right Foot',
    'Back Upper Back',
    'Back Lower Back',
    'Back Left Arm',
    'Back Right Arm',
    'Back Left Forearm',
    'Back Right Forearm',
    'Back Left Hand',
    'Back Right Hand',
    'Back Left Thigh',
    'Back Right Thigh',
    'Back Left Leg',
    'Back Right Leg',
    'Back Left Foot',
    'Back Right Foot',
  ];

  static String bodyLocation(AppState a, String key) {
    final map = <String, String>{
      'Front Head': 'ศีรษะด้านหน้า',
      'Front Neck': 'คอด้านหน้า',
      'Front Chest': 'หน้าอก',
      'Front Abdomen': 'หน้าท้อง',
      'Front Left Arm': 'แขนซ้ายด้านหน้า',
      'Front Right Arm': 'แขนขวาด้านหน้า',
      'Front Left Forearm': 'ท่อนแขนซ้ายด้านหน้า',
      'Front Right Forearm': 'ท่อนแขนขวาด้านหน้า',
      'Front Left Hand': 'มือซ้ายด้านหน้า',
      'Front Right Hand': 'มือขวาด้านหน้า',
      'Front Left Thigh': 'ต้นขาซ้ายด้านหน้า',
      'Front Right Thigh': 'ต้นขาขวาด้านหน้า',
      'Front Left Leg': 'ขาซ้ายด้านหน้า',
      'Front Right Leg': 'ขาขวาด้านหน้า',
      'Front Left Foot': 'เท้าซ้ายด้านหน้า',
      'Front Right Foot': 'เท้าขวาด้านหน้า',
      'Back Upper Back': 'หลังส่วนบน',
      'Back Lower Back': 'หลังส่วนล่าง',
      'Back Left Arm': 'แขนซ้ายด้านหลัง',
      'Back Right Arm': 'แขนขวาด้านหลัง',
      'Back Left Forearm': 'ท่อนแขนซ้ายด้านหลัง',
      'Back Right Forearm': 'ท่อนแขนขวาด้านหลัง',
      'Back Left Hand': 'มือซ้ายด้านหลัง',
      'Back Right Hand': 'มือขวาด้านหลัง',
      'Back Left Thigh': 'ต้นขาซ้ายด้านหลัง',
      'Back Right Thigh': 'ต้นขาขวาด้านหลัง',
      'Back Left Leg': 'ขาซ้ายด้านหลัง',
      'Back Right Leg': 'ขาขวาด้านหลัง',
      'Back Left Foot': 'เท้าซ้ายด้านหลัง',
      'Back Right Foot': 'เท้าขวาด้านหลัง',
    };
    final th = map[key];
    if (th != null) return a.translate(key, th);
    return key;
  }

  // --- Symptoms: internal storage key → localized checkbox label ---
  static String symptomLabel(AppState a, String key) {
    final m = <String, String>{
      'raised scar': 'แผลเป็นนูน',
      'Red marks': 'รอยแดง',
      'Sunbathe': 'อาบแดดบ่อย',
      'Fair skin': 'ผิวขาว',
      'The patient has a history of organ transplantation':
          'ผู้ป่วยเคยรับปลูกถ่ายอวัยวะ',
      'The patient has been exposed to arsenic':
          'ผู้ป่วยสัมผัสสารหนู',
      'The patient has photosensitivity': 'ผู้ป่วยแพ้แสง',
      'The patient has a history of skin disease':
          'ผู้ป่วยมีประวัติโรคผิวหนัง',
      'The patient has relatives who have had cancer.':
          'ผู้ป่วยมีญาติเป็นมะเร็ง',
    };
    final th = m[key];
    if (th != null) return a.translate(key, th);
    return key;
  }

  // --- Result screen ---
  static String riskHigh(AppState a) => a.translate('HIGH', 'สูง');
  static String riskModerate(AppState a) =>
      a.translate('MODERATE', 'ปานกลาง');
  static String riskLow(AppState a) => a.translate('LOW', 'ต่ำ');

  static String riskLevel(AppState a, String riskEn) {
    switch (riskEn) {
      case 'HIGH':
        return riskHigh(a);
      case 'MODERATE':
        return riskModerate(a);
      case 'LOW':
        return riskLow(a);
      default:
        return riskEn;
    }
  }

  /// Per-image decision on result screen (internal English → localized UI).
  static String resultImageDecisionStatus(AppState a, String raw) {
    final s = raw.trim();
    switch (s.toLowerCase()) {
      case 'none':
        return a.translate('None', 'ยังไม่ระบุ');
      case 'confirm':
        return a.translate('Confirm', 'ยืนยัน');
      case 'reject':
        return a.translate('Reject', 'ปฏิเสธ');
      case 'uncertain':
        return a.translate('Uncertain', 'ไม่แน่ใจ');
      default:
        return s.isEmpty ? a.translate('None', 'ยังไม่ระบุ') : s;
    }
  }
}
