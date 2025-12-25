package Cleaner.Royall;

import android.content.Context;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class AssetsPro {
    public static String getValue(Context ctx, String path, String mode) {
        if (ctx == null) return "";
        try (InputStream is = ctx.getAssets().open(path.startsWith("/") ? path.substring(1) : path);
             BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
            return sb.toString().trim();
        } catch (IOException e) {
            return "";
        }
    }
}
