import api from './api';

export const passwordResetAPI = {
  // Request to reset password (forgot password)
  requestPasswordReset: (username: string) => {
    return api.post('/forgot-password', {
      username
    });
  },
  
  // Actually reset the password with new password and token
  resetPassword: (token: string, newPassword: string, confirmNewPassword: string) => {
    return api.post('/reset-password', {
      token,
      new_password: newPassword,
      confirm_new_password: confirmNewPassword
    });
  }
};